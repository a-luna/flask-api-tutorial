"""Business logic for /auth API endpoints."""
from http import HTTPStatus

from flask import current_app, jsonify
from flask_restx import abort

from flask_api_tutorial import db
from flask_api_tutorial.api.auth.decorators import token_required
from flask_api_tutorial.models.token_blacklist import BlacklistedToken
from flask_api_tutorial.models.user import User
from flask_api_tutorial.util.datetime_util import (
    remaining_fromtimestamp,
    format_timespan_digits,
)


def process_registration_request(email, password):
    if User.find_by_email(email):
        abort(HTTPStatus.CONFLICT, f"{email} is already registered", status="fail")
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    access_token = new_user.encode_access_token()
    return _create_auth_successful_response(
        token=access_token.decode(),
        status_code=HTTPStatus.CREATED,
        message="successfully registered",
    )


def process_login_request(email, password):
    user = User.find_by_email(email)
    if not user or not user.check_password(password):
        abort(HTTPStatus.UNAUTHORIZED, "email or password does not match", status="fail")
    access_token = user.encode_access_token()
    return _create_auth_successful_response(
        token=access_token.decode(),
        status_code=HTTPStatus.OK,
        message="successfully logged in",
    )


@token_required
def get_logged_in_user():
    public_id = get_logged_in_user.public_id
    user = User.find_by_public_id(public_id)
    expires_at = get_logged_in_user.expires_at
    user.token_expires_in = format_timespan_digits(remaining_fromtimestamp(expires_at))
    return user


@token_required
def process_logout_request():
    access_token = process_logout_request.token
    expires_at = process_logout_request.expires_at
    blacklisted_token = BlacklistedToken(access_token, expires_at)
    db.session.add(blacklisted_token)
    db.session.commit()
    response_dict = dict(status="success", message="successfully logged out")
    return response_dict, HTTPStatus.OK


def _create_auth_successful_response(token, status_code, message):
    response = jsonify(
        status="success",
        message=message,
        access_token=token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
    )
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds if not current_app.config["TESTING"] else 5
