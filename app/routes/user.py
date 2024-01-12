from fastapi import APIRouter
from app.services.user import UserService
from app.schemas.user import (
    FullUserInfo,
    CreateResponseUserId,
    MultipleUserResponse
)


def create_user_routers() -> APIRouter:
    user_router = APIRouter(
        prefix="/user",
        tags=["User"]
    )
    user_service = UserService()

    # Always put general case on top

    @user_router.get("/all", response_model=MultipleUserResponse)
    async def get_user_pagination(start: int = 0, limit: int = 2):
        list_of_user_info, total = await user_service.get_user_paginated(start, limit)
        return MultipleUserResponse(multiple_user_info=list_of_user_info, total=total)

    @user_router.post("/add_user", response_model=CreateResponseUserId)
    async def add_user(full_user_info: FullUserInfo):
        user_id = await user_service.create_update_user(full_user_info)
        return CreateResponseUserId(user_id=user_id)

    @user_router.get("/{user_id}", response_model=FullUserInfo)
    async def get_user_by_id(user_id: int):
        full_user_info = await user_service.getUserInfo(user_id)

        # print("Docstring of getUserInfo: \n", getUserInfo.__doc__)
        return full_user_info

    @user_router.put("/{user_id}")
    async def update_user_info(user_id: int, full_user_info: FullUserInfo):
        await user_service.create_update_user(full_user_info, user_id)
        return None

    @user_router.delete("/{user_id")
    async def remove_user(user_id: int):
        await user_service.delete_user(user_id)
        return None

    return user_router
