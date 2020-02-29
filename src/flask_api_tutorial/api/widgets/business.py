"""Business logic for /widgets API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import abort, marshal

from flask_api_tutorial import db
from flask_api_tutorial.api.auth.decorators import token_required, admin_token_required
from flask_api_tutorial.api.widgets.dto import pagination_model, widget_name
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


@token_required
def retrieve_widget_list(page, per_page):
    pagination = Widget.query.paginate(page, per_page, error_out=False)
    response_data = marshal(pagination, pagination_model)
    response_data["links"] = _pagination_nav_links(pagination)
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination)
    response.headers["Total-Count"] = pagination.total
    return response


@token_required
def retrieve_widget(name):
    return Widget.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found in database."
    )


@admin_token_required
def update_widget(name, widget_dict):
    widget = Widget.find_by_name(name.lower())
    if widget:
        for k, v in widget_dict.items():
            setattr(widget, k, v)
        db.session.commit()
        message = f"'{name}' was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    try:
        valid_name = widget_name(name.lower())
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e), status="fail")
    widget_dict["name"] = valid_name
    return create_widget(widget_dict)


@admin_token_required
def delete_widget(name):
    widget = Widget.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found in database."
    )
    db.session.delete(widget)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


def _pagination_nav_links(pagination):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for("api.widget_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.widget_list", page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for(
            "api.widget_list", page=this_page - 1, per_page=per_page
        )
    if pagination.has_next:
        nav_links["next"] = url_for(
            "api.widget_list", page=this_page + 1, per_page=per_page
        )
    nav_links["last"] = url_for("api.widget_list", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")
