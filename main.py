from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

user_contents = {
    0: {
        "name": "default user",  # used to be "username": "test user"
        "liked_post": [1, 2, 3]
    },
}

profile_infos = {
    0: {
        "description": "default description",
        "long_bio": "default long bio"
    },
}


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


async def getUserInfo(user_id: int = 0) -> FullUserInfo:
    # Docstring
    """
    Endpoint to get user info with specific id
    :param user_id: int - unique id
    :return: FullUserInfo
    """

    # the key must same with User class

    profile_info = profile_infos[user_id]
    user_content = user_contents[user_id]

    full_user_info = {
        **profile_info,
        **user_content
    }

    profile_info = FullUserInfo(**full_user_info)

    return profile_info


async def get_user_paginated(start: int, limit: int) -> (list[FullUserInfo], int):
    keys = list(profile_infos.keys())
    list_of_users = []
    for i in range(0, len(keys), 1):
        if i < start:
            continue

        current_key = keys[i]
        user = await getUserInfo(current_key)
        list_of_users.append(user)
        if len(list_of_users) >= limit:
            break
    return list_of_users, len(list_of_users)


async def create_update_user(full_profile_info: FullUserInfo, new_user_id: Optional[int] = None) -> int:
    global profile_infos  # We need global because we're going to update them
    global user_contents

    if new_user_id is None:
        new_user_id = len(profile_infos)

    name = full_profile_info.username
    liked_post = full_profile_info.liked_post
    description = full_profile_info.description
    long_bio = full_profile_info.long_bio

    profile_infos[new_user_id] = {
        "description": description,
        "long_bio": long_bio
    }

    user_contents[new_user_id] = {
        "name": name,
        "liked_post": liked_post
    }

    return new_user_id


async def delete_user(user_id: int) -> None:
    global profile_infos
    global user_contents

    del profile_infos[user_id]
    del user_contents[user_id]


# Always put general case on top
@app.get("/user/me", response_model=FullUserInfo)
async def test_endpoint():
    full_user_info = await getUserInfo()
    return full_user_info


@app.get("/user/{user_id}", response_model=FullUserInfo)
async def get_user_by_id(user_id: int):
    full_user_info = await getUserInfo(user_id)

    # print("Docstring of getUserInfo: \n", getUserInfo.__doc__)
    return full_user_info


@app.put("/user/{user_id}")
async def update_user_info(user_id: int, full_user_info: FullUserInfo):
    await create_update_user(full_user_info, user_id)
    return None


@app.get("/users", response_model=MultipleUserResponse)
async def get_user_pagination(start: int = 0, limit: int = 2):
    list_of_user_info, total = await get_user_paginated(start, limit)
    return MultipleUserResponse(multiple_user_info=list_of_user_info, total=total)


@app.post("/users", response_model=CreateResponseUserId)
async def add_user(full_user_info: FullUserInfo):
    user_id = await create_update_user(full_user_info)
    return CreateResponseUserId(user_id=user_id)


@app.delete("/user/{user_id")
async def remove_user(user_id: int):
    await delete_user(user_id)
    return None
