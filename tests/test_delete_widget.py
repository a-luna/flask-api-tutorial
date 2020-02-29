"""Test cases for GET requests sent to the api.widget API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    DEFAULT_NAME,
    FORBIDDEN,
    login_user,
    create_widget,
    retrieve_widget,
    delete_widget,
)


def test_delete_widget(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    response = delete_widget(client, access_token, widget_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = retrieve_widget(client, access_token, widget_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_widget_no_admin_token(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = delete_widget(client, access_token, widget_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
