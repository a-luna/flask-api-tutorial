"""Parsers and serializers for /auth API endpoints."""
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser


auth_reqparser = RequestParser(bundle_errors=True)
auth_reqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
auth_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)
