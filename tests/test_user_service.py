import pytest


@pytest.mark.asyncio
async def test_delete_user_work_properly(user_service, user_contents, profile_infos):
    print("here", profile_infos)  # Add this line to check the contents

    user_to_delete = 0

    await user_service.delete_user(user_to_delete)

    assert user_to_delete not in user_contents
    assert user_to_delete not in profile_infos
