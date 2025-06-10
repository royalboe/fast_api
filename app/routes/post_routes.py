from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from datetime import datetime
from ..utils.oauth2 import get_current_user
from sqlmodel import select
from sqlalchemy import func
from typing import List, Optional

from ..models.post import Post as PostModel
from ..models.user import User as UserModel
from ..models.votes import Vote as VoteModel
from ..schema.schema import PostCreate, PostUpdate, PostResponseWithUser, PostWithVotesSchema
from ..utils.dependencies import SessionDep

router = APIRouter()

@router.get("/", response_model=List[PostWithVotesSchema])
def get_posts(
    session: SessionDep, 
    current_user: UserModel=Depends(get_current_user), 
    limit: int=Query(default=100, le=100), 
    offset: int=Query(default=0),
    search=""
    ):
    """
    Retrieve all blog posts.
    Returns a list of all stored posts.
    """
    try:
        if search:
            statement = (
                select(PostModel, func.count(VoteModel.post_id).label("votes"))
                .join(VoteModel, VoteModel.post_id == PostModel.id, isouter=True)
                .group_by(PostModel.id).filter(PostModel.title.contains(search))
                .order_by(PostModel.id.desc())
                .offset(offset)
                .limit(limit)
                )
        else:
            statement = select(PostModel, func.count(VoteModel.post_id).label("votes")).join(VoteModel, VoteModel.post_id == PostModel.id, isouter=True).group_by(PostModel.id).order_by(PostModel.id.desc()).offset(offset).limit(limit)
        # print(statement)
        posts = session.exec(statement).all()
        
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return posts

@router.get("/user-posts", response_model=List[PostResponseWithUser])
def get_my_posts(
    session:SessionDep, 
    current_user: UserModel = Depends(get_current_user),
    limit: int= Query(default=100, le=100),
    offset=0,
    search: Optional[str]=""
    ):
    """
    Retrieve all blog posts belonging to logged in user.
    Returns a list of all stored posts.
    """
    statement = (
        select(PostModel)
        .where(PostModel.author_id == current_user.id)
        .filter(PostModel.title.contains(search))
        .order_by(PostModel.id.desc())
        .offset(offset)
        .limit(limit)
    )
    try:
        posts = session.exec(statement).all()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return posts

@router.get("/{post_id}", response_model=PostWithVotesSchema)
def get_post(post_id: int, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
    """
    Get a post by its unique ID.
    If the post exists, returns it; otherwise, raises a 404 error.
    """
    try:
        statement = (
            select(PostModel, func.count(VoteModel.post_id).label("votes"))
            .join(VoteModel, VoteModel.post_id == PostModel.id, isouter=True)
            .group_by(PostModel.id)
            .where(PostModel.id == post_id)
        )
        post = session.exec(statement).first()
    except Exception as e:
        print(f"Error fetching post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    if not post:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    print(type(post))
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseWithUser)
def create_post(session: SessionDep, payload: PostCreate, current_user: UserModel = Depends(get_current_user)):
    """
    Create a new blog post with the given title and content.
    The post is validated using Pydantic and added to the in-memory storage.
    Returns the created post with its ID and timestamps.
    Raises a 500 error if there is a database error.
    """
    try:
        # post = PostModel(**payload.model_dump(exclude_unset=True))  # Unpack the payload into the model
        extra_data = {'author': current_user}
        post = PostModel.model_validate(payload, update=extra_data)
        session.add(post)
        session.commit()
        session.refresh(post)  # Refresh to get the ID and other defaults
    except Exception as e:
        print(f"Error creating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return post

@router.get("/latest/recent", response_model=PostResponseWithUser)
def get_latest_post(session: SessionDep, current_user: UserModel = Depends(get_current_user)):
    """
    Get the latest (most recently added) post.
    Returns the last post added to the storage.
    If no posts exist, raises a 404 error.
    """
    try:
        post = session.exec(select(PostModel).order_by(PostModel.created_at.desc())).first()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if not post:
        # Handle the case where no posts exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
    """
    Delete a post by its unique ID.
    If the post is found, it is removed from storage and a 204 status code is returned.
    If the post is not found, a 404 error is raised.
    """
    deleted_post = session.get(PostModel, post_id)
    if not deleted_post:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if deleted_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    try:
        session.delete(deleted_post)
        session.commit()  # Commit the deletion  
    except Exception as e:
        # Handle any database errors
        session.rollback()
        print(f"Error deleting post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")  

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostResponseWithUser, status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, payload: PostUpdate, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
    """
    Update an existing post by its unique ID using partial data.
    Returns the updated post or a 404 error if not found.
    """
    try:
        updated_post = session.get(PostModel, post_id)
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found"
            )
        
        if updated_post.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action"
            )
        update_data = payload.model_dump(exclude_unset=True)
        extra_data = {'updated_at': datetime.now().isoformat()}
        # Update the fields of the post
        # updated_post.sqlmodel_update(update_data, update=extra_data) # Outdated method, use setattr instead
        update_data.update(extra_data)

        for field, value in update_data.items():
            setattr(updated_post, field, value)
        session.add(updated_post)
        session.commit()
        session.refresh(updated_post)
    except HTTPException:
        raise
    except Exception as e:
        # Handle any database errors
        session.rollback()
        print(f"Error updating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    return updated_post