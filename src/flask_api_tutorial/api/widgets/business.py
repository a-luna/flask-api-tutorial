"""Business logic for /widgets API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import abort

from flask_api_tutorial import db
from flask_api_tutorial.api.auth.decorators import admin_token_required
from flask_api_tutorial.models.user import User
from flask_api_tutorial.models.widget import Widget


@admin_token_required
def create_widget(widget_dict):
    name = widget_dict["name"]
    if Widget.find_by_name(name):
        error = f"Widget name: {name} already exists, must be unique."
        abort(HTTPStatus.CONFLICT, error, status="fail")
    widget = Widget(**widget_dict)
    owner = User.find_by_public_id(create_widget.public_id)
    widget.owner_id = owner.id
    db.session.add(widget)
    db.session.commit()
    response = jsonify(status="success", message=f"New widget added: {name}.")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.widget", name=name)
    return response
