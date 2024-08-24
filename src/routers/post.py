from fastapi import APIRouter, HTTPException

from src.schemas.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComment,
)

router = APIRouter()

post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_recorded_id = len(post_table) + 1
    new_post = {**data, "id": last_recorded_id}
    post_table[last_recorded_id] = new_post
    return new_post


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    data = comment.model_dump()
    post = find_post(comment.post_id)

    if not post:
        raise HTTPException(
            404, detail=f"Post is not found with the post id {comment.post_id}"
        )

    last_recorded_id = len(comment_table) + 1
    new_comment = {**data, "id": last_recorded_id}
    comment_table[last_recorded_id] = new_comment
    return new_comment


@router.get("/comment/{post_id}")
async def get_comments_by_post_id(post_id: int):
    comments = list(comment_table.values())
    comments_by_post = list(
        filter(lambda comment: comment["post_id"] == post_id, comments)
    )
    return {"comments": comments_by_post}


@router.get("/", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())


@router.get("/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)

    if not post:
        raise HTTPException(404, detail=f"Post not found with id {post_id}")

    comments = list(comment_table.values())

    post_comments = filter(lambda comment: comment["post_id"] == post_id, comments)

    return {"post": post, "comments": post_comments}
