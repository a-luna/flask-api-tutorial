"""Unit tests for POST requests sent to api.widget_list API endpoint."""
from datetime import date, timedelta
from http import HTTPStatus

import pytest

from tests.util import (
    EMAIL,
    ADMIN_EMAIL,
    BAD_REQUEST,
    FORBIDDEN,
    DEFAULT_NAME,
    login_user,
    create_widget,
)


@pytest.mark.parametrize("widget_name", ["abc123", "widget-name", "new_widget1"])
def test_create_widget_valid_name(client, db, admin, widget_name):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token, widget_name=widget_name)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"New widget added: {widget_name}."
    assert "message" in response.json and response.json["message"] == success
    location = f"http://localhost/api/v1/widgets/{widget_name}"
    assert "Location" in response.headers and response.headers["Location"] == location


@pytest.mark.parametrize(
    "deadline_str",
    [
        date.today().strftime("%m/%d/%Y"),
        date.today().strftime("%Y-%m-%d"),
        (date.today() + timedelta(days=3)).strftime("%b %d %Y"),
    ],
)
def test_create_widget_valid_deadline(client, db, admin, deadline_str):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token, deadline_str=deadline_str)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"New widget added: {DEFAULT_NAME}."
    assert "message" in response.json and response.json["message"] == success
    location = f"http://localhost/api/v1/widgets/{DEFAULT_NAME}"
    assert "Location" in response.headers and response.headers["Location"] == location


@pytest.mark.parametrize(
    "deadline_str",
    [
        "1/1/1970",
        (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "a long time ago, in a galaxy far, far away",
    ],
)
def test_create_widget_invalid_deadline(client, db, admin, deadline_str):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token, deadline_str=deadline_str)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "errors" in response.json and "deadline" in response.json["errors"]


def test_create_widget_already_exists(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    response = create_widget(client, access_token)
    assert response.status_code == HTTPStatus.CONFLICT
    name_conflict = f"Widget name: {DEFAULT_NAME} already exists, must be unique."
    assert "message" in response.json and response.json["message"] == name_conflict


def test_create_widget_no_admin_token(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_widget(client, access_token)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
