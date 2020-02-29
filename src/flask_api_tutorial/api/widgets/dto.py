"""Parsers and serializers for /widgets API endpoints."""
import re
from datetime import date, datetime, time, timezone

from dateutil import parser
from flask_restx import Model
from flask_restx.fields import Boolean, DateTime, Integer, List, Nested, String, Url
from flask_restx.inputs import positive, URL
from flask_restx.reqparse import RequestParser

from flask_api_tutorial.util.datetime_util import make_tzaware, DATE_MONTH_NAME


def widget_name(name):
    """Validation method for a string containing only letters, numbers, '-' and '_'."""
    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must "
            "contain only letters, numbers, hyphen and underscore characters."
        )
    return name


def future_date_from_string(date_str):
    """Validation method for a date in the future, formatted as a string."""
    try:
        parsed_date = parser.parse(date_str)
    except ValueError:
        raise ValueError(
            f"Failed to parse '{date_str}' as a valid date. You can use any format "
            "recognized by dateutil.parser. For example, all of the strings below "
            "are valid ways to represent the same date: '2018-5-13' -or- '05/13/2018' "
            "-or- 'May 13 2018'."
        )

    if parsed_date.date() < date.today():
        raise ValueError(
            f"Successfully parsed {date_str} as "
            f"{parsed_date.strftime(DATE_MONTH_NAME)}. However, this value must be a "
            f"date in the future and {parsed_date.strftime(DATE_MONTH_NAME)} is BEFORE "
            f"{datetime.now().strftime(DATE_MONTH_NAME)}"
        )
    deadline = datetime.combine(parsed_date.date(), time.max)
    deadline_utc = make_tzaware(deadline, use_tz=timezone.utc)
    return deadline_utc


create_widget_reqparser = RequestParser(bundle_errors=True)
create_widget_reqparser.add_argument(
    "name",
    type=widget_name,
    location="form",
    required=True,
    nullable=False,
    case_sensitive=True,
)
create_widget_reqparser.add_argument(
    "info_url",
    type=URL(schemes=["http", "https"]),
    location="form",
    required=True,
    nullable=False,
)
create_widget_reqparser.add_argument(
    "deadline",
    type=future_date_from_string,
    location="form",
    required=True,
    nullable=False,
)

update_widget_reqparser = create_widget_reqparser.copy()
update_widget_reqparser.remove_argument("name")

pagination_reqparser = RequestParser(bundle_errors=True)
pagination_reqparser.add_argument("page", type=positive, required=False, default=1)
pagination_reqparser.add_argument(
    "per_page", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10
)

widget_owner_model = Model("Widget Owner", {"email": String, "public_id": String})

widget_model = Model(
    "Widget",
    {
        "name": String,
        "info_url": String,
        "created_at": String(attribute="created_at_str"),
        "created_at_iso8601": DateTime(attribute="created_at"),
        "created_at_rfc822": DateTime(attribute="created_at", dt_format="rfc822"),
        "deadline": String(attribute="deadline_str"),
        "deadline_passed": Boolean,
        "time_remaining": String(attribute="time_remaining_str"),
        "owner": Nested(widget_owner_model),
        "link": Url("api.widget"),
    },
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

pagination_model = Model(
    "Pagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(widget_model)),
    },
)
