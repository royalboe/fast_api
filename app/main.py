from fastapi import FastAPI, HTTPException, status, Body, Response, Depends
from pydantic import BaseModel, Field
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os
from sqlmodel import select, Session, SQLModel
from typing import Annotated, List
from contextlib import asynccontextmanager

from .models import Post
from .database import engine, get_session
from sqlmodel import SQLModel


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")

print(DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_USER)

def  create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]
# ----------------------------
# Pydantic model representing a blog post
# ----------------------------
class Post(BaseModel):
    # ID is automatically generated using a random number
    id: int = Field(default_factory=lambda: randrange(0, 1_000_000))
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # Optional rating field


# ----------------------------
# Database connection function
# ----------------------------
def connect_to_db():
    """
    Establish a connection to the PostgreSQL database using psycopg.
    Returns a connection object.
    """
    return psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

try:
    with connect_to_db() as conn:
        print("Database connected")
        # with conn.cursor() as cursor:
        #     cursor.execute("""
        #         CREATE TABLE IF NOT EXISTS fastapi (
        #             id SERIAL PRIMARY KEY,
        #             title TEXT NOT NULL,
        #             content TEXT NOT NULL,
        #             published BOOLEAN DEFAULT TRUE,
        #             rating FLOAT
        #         );
        #     """)
        #     conn.commit()
        #     print("Database connected and table created")
except Exception as e:
        print(f"Error during DB startup: {e}")
        



# ----------------------------
# In-memory storage class using a dictionary for fast access
# ----------------------------
class Storage:
    def __init__(self):
        # Dictionary for fast lookup and deletion by ID
        self.posts = {}  # Format: {id: Post}

    def generate_unique_id(self):
        # Generates a unique ID that is not already in use
        while True:
            new_id = randrange(0, 1_000_000)
            if new_id not in self.posts:
                return new_id

    def add_post(self, post: Post):
        # Ensure ID is unique before adding
        if post.id in self.posts:
            post.id = self.generate_unique_id()
        self.posts[post.id] = post

    def get_posts(self):
        # Return all posts as a list
        return list(self.posts.values())

    def get_post(self, id: int):
        # Return a specific post by ID, or None if not found
        return self.posts.get(id)

    def delete_post(self, id: int):
        # Delete a post by ID and return the deleted post or None
        return self.posts.pop(id, None)


# ----------------------------
# Initialize with some test data
# ----------------------------
storage = Storage()
storage.add_post(Post(title="Post 1", content="Content 1"))
storage.add_post(Post(title="Post 2", content="Content 2"))


# ----------------------------
# FastAPI Endpoints
# ----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)


@app.get('/health')
def health_check():
    """
    Health check endpoint to verify if the API is running.
    Returns a simple message indicating the API is healthy.
    """
    return {"status": "DB Created and API is running"}

@app.get("/")
def root():
    """
    Root route returns a simple welcome message.
    """
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    """
    Retrieve all blog posts.
    Returns a list of all stored posts.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM posts")
                posts = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Get a post by its unique ID.
    If the post exists, returns it; otherwise, raises a 404 error.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
                post = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    if not post:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post = Body(...)):
    """
    Create a new blog post with the given title and content.
    The post is validated using Pydantic and added to the in-memory storage.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    INSERT INTO 
                    posts (title, content, published, rating) 
                    VALUES (%s, %s, %s, %s) RETURNING * 
                    """, 
                    (payload.title, payload.content, payload.published, payload.rating)
                    )
                new_post = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    return {"data": new_post}


@app.get("/posts/latest/recent")
def get_latest_post():
    """
    Get the latest (most recently added) post.
    Returns the last post added to the storage.
    If no posts exist, raises a 404 error.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 5")
                posts = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if not posts:
        # Handle the case where no posts exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return {"data": posts}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Delete a post by its unique ID.
    If the post is found, it is removed from storage and a 204 status code is returned.
    If the post is not found, a 404 error is raised.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id, ))
                deleted_post = cursor.fetchone()
    except Exception as e:
        print(f"Error deleting post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    # Check if the post was deleted
    if not deleted_post:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # Return a 204 response without any content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, payload: Post = Body(...)):
    """
    Update an existing post by its unique ID.
    If the post exists, it is updated with the new data; otherwise, a 404 error is raised.
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    UPDATE posts
                    SET title = %s, content = %s, published = %s, rating = %s
                    WHERE id = %s
                    RETURNING *;
                    """,
                    (payload.title, payload.content, payload.published, payload.rating, post_id)
                )
                updated_post = cursor.fetchone()
                conn.commit()  # Ensure changes are saved

    except Exception as e:
        print(f"Error updating post: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    return {"data": updated_post}
