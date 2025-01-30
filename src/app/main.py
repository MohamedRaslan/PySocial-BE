import logging
from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
from random import randrange
import os
from fastapi import  FastAPI, HTTPException, Response , status
from pydantic import BaseModel


# Get the logger for the app
logger = logging.getLogger("uvicorn.error")

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup logic
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "8000")
    logger.info("App documentation available at:")
    logger.info("Swagger :: http://%s:%s/redoc", host, port)
    logger.info("Redoc   :: http://%s:%s/docs\n", host, port)

    yield  # The app is now running

    # Shutdown logic (if needed)
    logger.info("Shutting down...")

# Pass the lifespan handler to the FastAPI app
app = FastAPI(lifespan=lifespan)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"title": "Hello World", "content": "This is my first post", "published": True, "rating": 5 , "id": 1},
           {"title": "Second Post", "content": "This is my second post", "published": True, "rating": 4, "id": 2},
           {"title": "Third Post", "content": "This is my third post", "published": False, "rating": 3, "id": 3}]


def find_index_post(id):
    for i in range(len(my_post)):
        if my_post[i]["id"] == id:
            return i
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

    index = find_index_post(post_id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"data": my_post[index]}


# create a post
@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(9, 99999999999999)
    my_post.append(post_dict)
    return {"data": post_dict }


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    index = find_index_post(post_id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    post_dict = post.model_dump()
    index = find_index_post(post_id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post_dict["id"] = my_post[index]["id"]
    my_post[index] = post_dict

    return {"data": post_dict}


