from fastapi import FastAPI, Response, status, HTTPException
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
    
    def get_post(self, id: int):
        for post in self.posts:
            if post["id"] == id:
                return post
        return None
    
    def delete_post(self, id: int):
        for index, post in enumerate(self.posts):
            if post["id"] == id:
                self.posts.pop(index)
                return True
        return False
    
storage = Storage()

storage.add_post(Post(title="Post 1", content="Content 1").model_dump())
storage.add_post(Post(title="Post 2", content="Content 2").model_dump())

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": storage.get_posts()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
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

def find_post(id: int):
    """
    Find a post by id.
    """
    for post in storage.get_posts():
        if post["id"] == id:
            return post
    return None

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    """
    Get a post by id.
    """
    post = find_post(id)
    # If the post is found, return it
    if post:
        return {"data": post}
    # If the post is not found, return a 404 error
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"Post with id: {id} not found"}
    # OR raise an HTTPException
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")


@app.get("/posts/latest/recent")
def get_latest_post():
    """
    Get the latest post.
    """
    return {"data": storage.get_posts()[-1]}  

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Delete a post by id.
    """
    if storage.delete_post(id):
        return # {"message": f"Post with id: {id} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found") 