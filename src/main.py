from fastapi import FastAPI

from src.models.post import UserPost, UserPostIn

app = FastAPI()


post_table = {}


@app.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_recorded_id = len(post_table) + 1
    new_post = {**data, "id": last_recorded_id}
    post_table[last_recorded_id] = new_post
    return new_post


@app.get("/posts", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())


@app.get("/")
async def root():
    return {"message": "Hello Fast API"}
