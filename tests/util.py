"""Shared functions and constants for unit tests."""
from flask import url_for

EMAIL = "new_user@email.com"
PASSWORD = "test1234"
BAD_REQUEST = "Input payload validation failed"


def register_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )
