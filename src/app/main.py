from random import randrange
from typing import Optional
from fastapi import  FastAPI, HTTPException , status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"title": "Hello World", "content": "This is my first post", "published": True, "rating": 5 , "id": 1},
           {"title": "Second Post", "content": "This is my second post", "published": True, "rating": 4, "id": 2},
           {"title": "Third Post", "content": "This is my third post", "published": False, "rating": 3, "id": 3}]

def find_post(id):
    for post in my_post:
        if post["id"] == id:
            return post
    return None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_post}

@app.get("/posts/latest")
async def get_latest_post():
    return {"data": my_post[-1]}

@app.get("/posts/{post_id}")
async def get_post(post_id: int ):

    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"data": post}


# create a post
@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(9, 99999999999999)
    my_post.append(post_dict)
    return {"data": post_dict }