from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import db


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namle = db.Column(db.String(80), unique=True)
    description = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

