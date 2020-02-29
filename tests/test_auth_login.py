"""Unit tests for api.auth_login API endpoint."""
from http import HTTPStatus

from flask_api_tutorial.models.user import User
from tests.util import EMAIL, register_user, login_user

SUCCESS = "successfully logged in"
UNAUTHORIZED = "email or password does not match"


def test_login(client, db):
    register_user(client)
    response = login_user(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    result = User.decode_access_token(access_token)
    assert result.success
    token_payload = result.value
    assert not token_payload["admin"]
    user = User.find_by_public_id(token_payload["public_id"])
    assert user and user.email == EMAIL


def test_login_email_does_not_exist(client, db):
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == UNAUTHORIZED
    assert "access_token" not in response.json
