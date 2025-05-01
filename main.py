from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
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

storage.add_post(Post(title="Post 1", content="Content 1"))
storage.add_post(Post(title="Post 2", content="Content 2"))

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
    payload.model_dump() # To convert pydantic to dict in v2.0
    # Simulate saving the post to a database or processing it 
    print(payload)
    return {
        "data": payload
        }