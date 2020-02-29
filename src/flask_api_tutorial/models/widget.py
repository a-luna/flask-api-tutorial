"""Class definition for Widget model."""
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.hybrid import hybrid_property

from flask_api_tutorial import db
from flask_api_tutorial.util.datetime_util import (
    utc_now,
    format_timedelta_str,
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
)


class Widget(db.Model):
    """Widget model for a generic resource in a REST API."""

    __tablename__ = "widget"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    info_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utc_now)
    deadline = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("site_user.id"), nullable=False)
    owner = db.relationship("User", backref=db.backref("widgets"))

    def __repr__(self):
        return f"<Widget name={self.name}, info_url={self.info_url}>"

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def deadline_str(self):
        deadline_utc = make_tzaware(self.deadline, use_tz=timezone.utc, localize=False)
        return localized_dt_string(deadline_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def deadline_passed(self):
        return datetime.now(timezone.utc) > self.deadline.replace(tzinfo=timezone.utc)

    @hybrid_property
    def time_remaining(self):
        time_remaining = self.deadline.replace(tzinfo=timezone.utc) - utc_now()
        return time_remaining if not self.deadline_passed else timedelta(0)

    @hybrid_property
    def time_remaining_str(self):
        timedelta_str = format_timedelta_str(self.time_remaining)
        return timedelta_str if not self.deadline_passed else "No time remaining"

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
