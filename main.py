from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}


@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": f"Title: {payload['title']}, Content: {payload['content']}"}