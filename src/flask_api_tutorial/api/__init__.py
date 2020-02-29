"""API blueprint configuration."""
from flask import Blueprint
from flask_restx import Api

from flask_api_tutorial.api.auth.endpoints import auth_ns
from flask_api_tutorial.api.widgets.endpoints import widget_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation site!",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(widget_ns, path="/widgets")
