from app.schemas.user import FullUserInfo
from typing import Optional
from app.exceptions import UserNotFound


class UserService:
    def __init__(self, user_contents: dict, profile_infos: dict):
        self.user_contents = user_contents
        self.profile_infos = profile_infos

    async def get_user_paginated(self, start: int, limit: int) -> (list[FullUserInfo], int):
        keys = list(self.profile_infos.keys())
        list_of_users = []
        for i in range(0, len(keys), 1):
            if i < start:
                continue

            current_key = keys[i]
            user = await self.getUserInfo(current_key)
            list_of_users.append(user)
            if len(list_of_users) >= limit:
                break
        return list_of_users, len(list_of_users)

    async def getUserInfo(self, user_id: int = 0) -> FullUserInfo:
        # Docstring
        """
        Endpoint to get user info with specific id
        :param user_id: int - unique id
        :return: FullUserInfo
        """
        if user_id not in self.profile_infos:
            raise UserNotFound(user_id=user_id)
        # the key must same with User class

        profile_info = self.profile_infos[user_id]
        user_content = self.user_contents[user_id]

        full_user_info = {
            **profile_info,
            **user_content
        }

        profile_info = FullUserInfo(**full_user_info)

        return profile_info

    async def create_update_user(self, full_profile_info: FullUserInfo, new_user_id: Optional[int] = None) -> int:

        if new_user_id is None:
            new_user_id = len(self.profile_infos)

        name = full_profile_info.username
        liked_post = full_profile_info.liked_post
        description = full_profile_info.description
        long_bio = full_profile_info.long_bio

        self.profile_infos[new_user_id] = {
            "description": description,
            "long_bio": long_bio
        }

        self.user_contents[new_user_id] = {
            "name": name,
            "liked_post": liked_post
        }

        return new_user_id

    async def delete_user(self, user_id: int):

        if user_id not in self.profile_infos:
            raise UserNotFound(user_id=user_id)

        del self.profile_infos[user_id]
        del self.user_contents[user_id]
