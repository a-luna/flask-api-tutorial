"""API endpoint definitions for /auth namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_tutorial.api.auth.dto import auth_reqparser, user_model
from flask_api_tutorial.api.auth.business import (
    process_registration_request,
    process_login_request,
    get_logged_in_user,
    process_logout_request,
)

auth_ns = Namespace(name="auth", validate=True)
auth_ns.models[user_model.name] = user_model


@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/register."""

    @auth_ns.expect(auth_reqparser)
    @auth_ns.response(int(HTTPStatus.CREATED), "New user was successfully created.")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Register a new user and return an access token."""
        request_data = auth_reqparser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")
        return process_registration_request(email, password)


@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/login."""

    @auth_ns.expect(auth_reqparser)
    @auth_ns.response(int(HTTPStatus.OK), "Login succeeded.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "email or password does not match")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Authenticate an existing user and return an access token."""
        request_data = auth_reqparser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")
        return process_login_request(email, password)


@auth_ns.route("/user", endpoint="auth_user")
class GetUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/user."""

    @auth_ns.doc(security="Bearer")
    @auth_ns.response(int(HTTPStatus.OK), "Token is currently valid.", user_model)
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.marshal_with(user_model)
    def get(self):
        """Validate access token and return user info."""
        return get_logged_in_user()


@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    """Handles HTTP requests to URL: /auth/logout."""

    @auth_ns.doc(security="Bearer")
    @auth_ns.response(int(HTTPStatus.OK), "Log out succeeded, token is no longer valid.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Add token to blacklist, deauthenticating the current user."""
        return process_logout_request()
