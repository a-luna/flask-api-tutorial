"""API endpoint definitions for /auth namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_tutorial.api.auth.dto import auth_reqparser
from flask_api_tutorial.api.auth.business import process_registration_request

auth_ns = Namespace(name="auth", validate=True)


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
