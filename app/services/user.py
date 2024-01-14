from app.schemas.user import FullUserInfo
from typing import Optional
from app.exceptions import UserNotFound


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


class UserService:
    def __init__(self):
        pass

    async def get_user_paginated(self, start: int, limit: int) -> (list[FullUserInfo], int):
        keys = list(profile_infos.keys())
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    async def delete_user(user_id: int) -> None:
        global profile_infos
        global user_contents

        if user_id not in profile_infos:
            raise UserNotFound(user_id=user_id)

        del profile_infos[user_id]
        del user_contents[user_id]
