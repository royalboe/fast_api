from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    id: int = Field(default_factory=lambda: randrange(0, 1_000_000)) # generates a value at the time of model creation
    title: str
    content: str
    published: bool = True
    # rating: float | None = None
    rating: Optional[float] = None

class Storage():
    def __init__(self):
        self.posts = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def get_posts(self):
        return self.posts
    
storage = Storage()

storage.add_post(Post(title="Post 1", content="Content 1").model_dump())
storage.add_post(Post(title="Post 2", content="Content 2").model_dump())

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": storage.get_posts()}


@app.post("/posts")
def create_posts(payload: Post = Body(...)):
    """
    Create a post with the given title and content.
    """
    # Validate the payload using Pydantic
    # payload.dict() To convert pydantic to dict
    post = payload.model_dump() # To convert pydantic to dict in v2.0
    storage.add_post(post) # Simulate saving the post to a database or processing it 
    print(post)
    return {
        "data": post
        }