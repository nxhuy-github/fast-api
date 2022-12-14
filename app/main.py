from turtle import pos
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "title 1", "content": "some content", "id": 1},
    {"title": "title 2", "content": "i like me", "id": 2}
]

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    print(id, type(id))
    for post in my_posts:
        if post["id"] == id:
            return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for idx, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    post_dict = post.dict()
    post_dict["id"] = id
    for idx, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[idx] = post_dict
    return {'message': 'updated post'}
