from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select
from typing import List

from ..models.post import Post as PostModel
from ..schema.post_schema import PostCreate, PostUpdate, PostResponse, PostBase
from ..dependencies import SessionDep

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
def get_posts(session: SessionDep):
    """
    Retrieve all blog posts.
    Returns a list of all stored posts.
    """
    try:
        posts = session.exec(select(PostModel)).all()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return posts


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, session: SessionDep):
    """
    Get a post by its unique ID.
    If the post exists, returns it; otherwise, raises a 404 error.
    """
    try:
        post = session.get(PostModel, post_id)
    except Exception as e:
        print(f"Error fetching post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    if not post:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(session: SessionDep, payload: PostCreate):
    """
    Create a new blog post with the given title and content.
    The post is validated using Pydantic and added to the in-memory storage.
    """
    print('trying to create post')
    try:
        post = PostModel(**payload.model_dump(exclude_unset=True))  # Unpack the payload into the model 
        session.add(post)
        session.commit()
        session.refresh(post)  # Refresh to get the ID and other defaults
    except Exception as e:
        print(f"Error creating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return post

@router.get("/latest/recent", response_model=PostResponse)
def get_latest_post(session: SessionDep):
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
def delete_post(post_id: int, session: SessionDep):
    """
    Delete a post by its unique ID.
    If the post is found, it is removed from storage and a 204 status code is returned.
    If the post is not found, a 404 error is raised.
    """
    deleted_post = session.get(PostModel, post_id)
    if not deleted_post:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    try:
        session.delete(deleted_post)
        session.commit()  # Commit the deletion  
    except Exception as e:
        print(f"Error deleting post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")  

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostResponse, status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, payload: PostUpdate, session: SessionDep):
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

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(updated_post, field, value)

        session.commit()
        session.refresh(updated_post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    return updated_post