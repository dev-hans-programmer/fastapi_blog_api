from pydantic import BaseModel


class UserPostIn(BaseModel):
    title: str


class UserPost(UserPostIn):
    id: int


class CommentIn(BaseModel):
    title: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComment(BaseModel):
    post: UserPost
    comments: list[Comment]
