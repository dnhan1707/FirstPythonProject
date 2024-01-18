import pytest
from app.services.user import UserService


@pytest.fixture
def user_contents():
    val = {
        0: {
            "name": "default user",  # used to be "username": "tests user"
            "liked_post": [1, 2, 3]
        }
    }
    return val


@pytest.fixture
def profile_infos():
    val = {
        0: {
            "description": "default description",
            "long_bio": "default long bio"
        }
    }
    return val


@pytest.fixture
def user_service(user_contents, profile_infos) -> UserService:
    user_service = UserService(user_contents, profile_infos)
    return user_service
