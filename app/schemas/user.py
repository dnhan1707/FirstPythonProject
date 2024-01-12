from pydantic import BaseModel, Field


class User(BaseModel):
    # Field is for constraint or give username some properties
    username: str = Field(
        alias="name",
        title="title for username",
        description="description of the username",
        min_length=1,
        # max_length=25,  we don;t need this anymore bc we have the Config class in this User class
        default="user - default user name bc no value assigned"
    )
    liked_post: list[int] = Field(
        description="list of integer",
        min_items=1
    )

    class Config:
        max_anystr_length = 20  # Must use the same vocabulary


class FullUserInfo(User):
    description: str
    long_bio: str


class MultipleUserResponse(BaseModel):
    multiple_user_info: list[FullUserInfo]
    total: int


class CreateResponseUserId(BaseModel):
    user_id: int
