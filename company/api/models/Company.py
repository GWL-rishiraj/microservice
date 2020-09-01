from api.core import Mixin
from .base import db


class Company(Mixin, db.Model):
    """Company Table."""

    __tablename__ = "company"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    emails = db.relationship("Email", backref="emails")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Company {self.name}>"
