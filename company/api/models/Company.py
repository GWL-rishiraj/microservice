from api.core import Mixin
from .base import db
from sqlalchemy.ext.declarative import as_declarative,declared_attr
from sqlalchemy.sql import func

'''
@as_declarative()
class BaseModel(db.Model):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id =  db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
'''
class CompanyType(Mixin, db.Model):
    """Company Table."""

    __tablename__ = "company_type"
    id =  db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    type = db.Column(db.String, nullable=False)

class Company(Mixin, db.Model):
    """Company Table."""

    __tablename__ = "company"
    id =  db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    name = db.Column(db.String, nullable=False)
    company_type = db.Column(db.Integer, db.ForeignKey('company_type.id'))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    phone =  db.Column(db.String, nullable=False)
    MSA =  db.Column(db.String, nullable=False)
    NDS =  db.Column(db.String, nullable=False)
    url =  db.Column(db.String, nullable=False)
    logo =  db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Company {self.name}>"
