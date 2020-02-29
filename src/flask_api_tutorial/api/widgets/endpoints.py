"""API endpoint definitions for /widgets namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_tutorial.api.widgets.dto import (
    create_widget_reqparser,
    update_widget_reqparser,
    pagination_reqparser,
    widget_owner_model,
    widget_model,
    pagination_links_model,
    pagination_model,
)
from flask_api_tutorial.api.widgets.business import (
    create_widget,
    retrieve_widget_list,
    retrieve_widget,
    update_widget,
    delete_widget,
)

widget_ns = Namespace(name="widgets", validate=True)
widget_ns.models[widget_owner_model.name] = widget_owner_model
widget_ns.models[widget_model.name] = widget_model
widget_ns.models[pagination_links_model.name] = pagination_links_model
widget_ns.models[pagination_model.name] = pagination_model


@widget_ns.route("", endpoint="widget_list")
@widget_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widget_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widget_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class WidgetList(Resource):
    """Handles HTTP requests to URL: /widgets."""

    @widget_ns.doc(security="Bearer")
    @widget_ns.response(HTTPStatus.OK, "Retrieved widget list.", pagination_model)
    @widget_ns.expect(pagination_reqparser)
    def get(self):
        """Retrieve a list of widgets."""
        request_data = pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_widget_list(page, per_page)

    @widget_ns.doc(security="Bearer")
    @widget_ns.response(int(HTTPStatus.CREATED), "Added new widget.")
    @widget_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @widget_ns.response(int(HTTPStatus.CONFLICT), "Widget name already exists.")
    @widget_ns.expect(create_widget_reqparser)
    def post(self):
        """Create a widget."""
        widget_dict = create_widget_reqparser.parse_args()
        return create_widget(widget_dict)


@widget_ns.route("/<name>", endpoint="widget")
@widget_ns.param("name", "Widget name")
@widget_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widget_ns.response(int(HTTPStatus.NOT_FOUND), "Widget not found.")
@widget_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widget_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Widget(Resource):
    """Handles HTTP requests to URL: /widgets/{name}."""

    @widget_ns.doc(security="Bearer")
    @widget_ns.response(int(HTTPStatus.OK), "Retrieved widget.", widget_model)
    @widget_ns.marshal_with(widget_model)
    def get(self, name):
        """Retrieve a widget."""
        return retrieve_widget(name)

    @widget_ns.doc(security="Bearer")
    @widget_ns.response(int(HTTPStatus.OK), "Widget was updated.", widget_model)
    @widget_ns.response(int(HTTPStatus.CREATED), "Added new widget.")
    @widget_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @widget_ns.expect(update_widget_reqparser)
    def put(self, name):
        """Update a widget."""
        widget_dict = update_widget_reqparser.parse_args()
        return update_widget(name, widget_dict)

    @widget_ns.doc(security="Bearer")
    @widget_ns.response(int(HTTPStatus.NO_CONTENT), "Widget was deleted.")
    @widget_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, name):
        """Delete a widget."""
        return delete_widget(name)
