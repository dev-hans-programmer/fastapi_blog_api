from pydantic import BaseModel


class UserPostIn(BaseModel):
    title: str


class UserPost(UserPostIn):
    id: int
