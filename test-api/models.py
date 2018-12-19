import sys
import os

from app import db

class Person(db.Model) :
	__tablename__ = "person_table"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(32))

