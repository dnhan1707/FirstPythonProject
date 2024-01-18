import pytest


def test_delete_user_endpoint(valid_user_id, testing_app):
    response = testing_app.delete(f"/user/{valid_user_id}")
    assert response.status_code == 200

    second_response = testing_app.delete(f"/user/{valid_user_id}")
    assert second_response.status_code == 404


def test_fail_delete_user_endpoint(invalid_user_id, testing_app):
    response = testing_app.delete(f"/user/{invalid_user_id}")
    assert response.status_code == 404


def test_get_user_endpoint(valid_user_id, testing_app):
    response = testing_app.get(f"/user/{valid_user_id}")
    assert response.json()["name"] == "default user"


def test_put_user_endpoint(testing_app, sample_full_user_info):
    user_id = 0
    response = testing_app.put(f"/user/{user_id}", json=sample_full_user_info.dict())
    assert response.status_code == 200

    create_user_id = 1
    second_response = testing_app.put(f"/user/{create_user_id}", json=sample_full_user_info.dict())
    assert second_response.status_code == 200


def test_rate_limit(rate_limit, testing_app, valid_user_id):
    for i in range(rate_limit):
        response = testing_app.get(f"/user/{valid_user_id}")
        if 'x_app_rate_limit' not in response.headers:
            assert response.status_code == 429
