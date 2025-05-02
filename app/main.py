from fastapi import FastAPI, HTTPException, status, Body, Response
from pydantic import BaseModel, Field
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")

print(DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_USER)

app = FastAPI()

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
try:
    with psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    ) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            # Example query to fetch all posts
            print("Connected to the database")
            # cursor.execute("SELECT * FROM fastapi")
            # posts = cursor.fetchall()
            # print(posts)  # Print fetched posts for debugging
except Exception as e:
    print(f"Error connecting to the database: {e}")



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
    return {"data": [post.model_dump() for post in storage.get_posts()]}


@app.get("/posts/{id}")
def get_post(id: int):
    """
    Get a post by its unique ID.
    If the post exists, returns it; otherwise, raises a 404 error.
    """
    post = storage.get_post(id)
    if not post:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post.model_dump()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post = Body(...)):
    """
    Create a new blog post with the given title and content.
    The post is validated using Pydantic and added to the in-memory storage.
    """
    storage.add_post(payload)
    return {"data": payload.model_dump()}


@app.get("/posts/latest/recent")
def get_latest_post():
    """
    Get the latest (most recently added) post.
    Returns the last post added to the storage.
    If no posts exist, raises a 404 error.
    """
    posts = storage.get_posts()
    if not posts:
        # Handle the case where no posts exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return {"data": posts[-1].model_dump()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Delete a post by its unique ID.
    If the post is found, it is removed from storage and a 204 status code is returned.
    If the post is not found, a 404 error is raised.
    """
    deleted = storage.delete_post(id)
    if not deleted:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # Return a 204 response without any content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, payload: Post = Body(...)):
    """
    Update an existing post by its unique ID.
    If the post exists, it is updated with the new data; otherwise, a 404 error is raised.
    """
    post = storage.get_post(id)
    if not post:
        # Raise 404 if post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # Update the post with new data
    post.title = payload.title
    post.content = payload.content
    post.published = payload.published
    post.rating = payload.rating
    return {"data": post.model_dump()}
