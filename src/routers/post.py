from fastapi import APIRouter

from src.models.post import UserPost, UserPostIn

router = APIRouter()

post_table = {}


@router.post("/", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_recorded_id = len(post_table) + 1
    new_post = {**data, "id": last_recorded_id}
    post_table[last_recorded_id] = new_post
    return new_post


@router.get("/", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
