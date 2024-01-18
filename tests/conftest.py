import pytest
from app.schemas.user import FullUserInfo


@pytest.fixture(scope="function")
def valid_user_id():
    return 0


@pytest.fixture(scope="function")
def invalid_user_id():
    return 1


@pytest.fixture(scope="function")
def sample_full_user_info() -> FullUserInfo:
    return FullUserInfo(description="test description",
                        long_bio="test long bio",
                        username="test username",
                        liked_post=[1, 2, 3])


@pytest.fixture(scope="function")
def rate_limit() -> int:
    return 50
