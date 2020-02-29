"""Test cases for GET requests sent to the api.widget_list API endpoint."""
from datetime import date, timedelta
from http import HTTPStatus

from tests.util import ADMIN_EMAIL, login_user, create_widget, retrieve_widget_list


NAMES = [
    "widget1",
    "second_widget",
    "widget-thrice",
    "tetraWIDG",
    "PENTA-widg-GON-et",
    "hexa_widget",
    "sep7",
]

URLS = [
    "http://www.one.com",
    "https://www.two.net",
    "https://www.three.edu",
    "http://www.four.dev",
    "http://www.five.io",
    "https://www.six.tech",
    "https://www.seven.dot",
]

DEADLINES = [
    date.today().strftime("%m/%d/%y"),
    (date.today() + timedelta(days=3)).strftime("%m/%d/%y"),
    (date.today() + timedelta(days=5)).strftime("%m/%d/%y"),
    (date.today() + timedelta(days=10)).strftime("%m/%d/%y"),
    (date.today() + timedelta(days=17)).strftime("%m/%d/%y"),
    (date.today() + timedelta(days=23)).strftime("%m/%d/%y"),
    (date.today() + timedelta(days=78)).strftime("%m/%d/%y"),
]


def test_retrieve_paginated_widget_list(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    # ADD SEVEN WIDGET INSTANCES TO DATABASE
    for i in range(0, len(NAMES)):
        response = create_widget(
            client,
            access_token,
            widget_name=NAMES[i],
            info_url=URLS[i],
            deadline_str=DEADLINES[i],
        )
        assert response.status_code == HTTPStatus.CREATED

    # REQUEST PAGINATED LIST OF WIDGETS: 5 PER PAGE, PAGE #1
    response = retrieve_widget_list(client, access_token, page=1, per_page=5)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 2
    assert "items_per_page" in response.json and response.json["items_per_page"] == 5
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 5

    # VERIFY ATTRIBUTES OF WIDGETS #1-5
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "info_url" in item and item["info_url"] == URLS[i]
        assert "deadline" in item and DEADLINES[i] in item["deadline"]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF WIDGETS: 5 PER PAGE, PAGE #2
    response = retrieve_widget_list(client, access_token, page=2, per_page=5)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #2
    assert "has_prev" in response.json and response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 2
    assert "total_pages" in response.json and response.json["total_pages"] == 2
    assert "items_per_page" in response.json and response.json["items_per_page"] == 5
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 2

    # VERIFY ATTRIBUTES OF WIDGETS #6-7
    for i in range(5, response.json["total_items"]):
        item = response.json["items"][i - 5]
        assert "name" in item and item["name"] == NAMES[i]
        assert "info_url" in item and item["info_url"] == URLS[i]
        assert "deadline" in item and DEADLINES[i] in item["deadline"]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF WIDGETS: 10 PER PAGE, PAGE #1
    response = retrieve_widget_list(client, access_token, page=1, per_page=10)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 1
    assert "items_per_page" in response.json and response.json["items_per_page"] == 10
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 7

    # VERIFY ATTRIBUTES OF WIDGETS #1-7
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "info_url" in item and item["info_url"] == URLS[i]
        assert "deadline" in item and DEADLINES[i] in item["deadline"]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF WIDGETS: DEFAULT PARAMETERS
    response = retrieve_widget_list(client, access_token)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 1
    assert "items_per_page" in response.json and response.json["items_per_page"] == 10
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 7

    # VERIFY ATTRIBUTES OF WIDGETS #1-7
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "info_url" in item and item["info_url"] == URLS[i]
        assert "deadline" in item and DEADLINES[i] in item["deadline"]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL
