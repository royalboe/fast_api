from fastapi import FastAPI, HTTPException, status, Response, Depends, Body
from dotenv import load_dotenv
from sqlmodel import select, Session, SQLModel
from sqlalchemy import text
from typing import Annotated, List
from contextlib import asynccontextmanager

from .models import Post as PostModel
from .database import get_session, create_db_and_tables

load_dotenv()

SessionDep = Annotated[Session, Depends(get_session)]

# ---------------------------A-
# FastAPI Endpoints
# ----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check(session: SessionDep):
    try:
        session.exec(text('SELECT 1'))  # lightweight DB check
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/")
def root():
    """
    Root route returns a simple welcome message.
    """
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[PostModel])
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


@app.get("/posts/{post_id}")
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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(session: SessionDep, post: PostModel):
    """
    Create a new blog post with the given title and content.
    The post is validated using Pydantic and added to the in-memory storage.
    """
    print('trying to create post')
    try:
        # post = PostModel(**payload.model_dump(exclude_unset=True))  # Unpack the payload into the model 
        session.add(post)
        session.commit()
        session.refresh(post)  # Refresh to get the ID and other defaults
    except Exception as e:
        print(f"Error creating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return post

@app.get("/posts/latest/recent")
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


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, payload: PostModel, session: SessionDep):
    """
    Update an existing post by its unique ID.
    If the post exists, it is updated with the new data; otherwise, a 404 error is raised.
    """
    updated_post = session.get(PostModel, post_id)
    if not updated_post:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    # updated_post.title = payload.title or updated_post.title  # Keep the existing title if not provided
    # updated_post.content = payload.content or updated_post.content  # Keep the existing content if not provided
    # updated_post.published = payload.published or updated_post.published  # Keep the existing published status if not provided
    # updated_post.rating = payload.rating or updated_post.rating  # Keep the existing rating if not provided
    updated_post
    try:
        # Commit the changes to the database
        session.commit()
        session.refresh(updated_post)
    except Exception as e:
        print(f"Error updating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    return updated_post
