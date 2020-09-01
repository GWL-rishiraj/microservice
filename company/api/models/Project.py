from api.core import Mixin
from .base import db

class Project(Mixin, db.Model):
	"""Project Table."""

	__tablename__ = "project"

	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String, nullable=False)

	def __init__(self, name: str):
		self.name = name

	def __repr__(self):
		return f"<Project: {self.name}>"


class ProjectAssigned(Mixin, db.Model):
	"""ProjectAssigned Table."""

	__tablename__ = "project_assigned"

	id = db.Column(db.Integer, unique=True, primary_key=True)
	user_id = db.Column(db.Integer)
	name = db.Column(db.String, nullable=False)
	project = db.Column(db.Integer, db.ForeignKey('project.id'))

	def __init__(self, name: str):
		self.name = name

	def __repr__(self):
		return f"<Project: {self.name}>"

