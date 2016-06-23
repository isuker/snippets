from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from app.lib.util import DenormalizedText, dbFunctions, slugify,\
    tomarkdown, domain

from app.models import User
from app import db,testbed,testset

from datetime import datetime
from werkzeug import cached_property


class TestSet(db.Model, dbFunctions):
    __tablename__ = "testsets"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True)

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    __mapper_args__ = {'order_by' : id.desc()}


    # FIXME Test step

    def __init__(self, filename, author_id):
        self.filename = filename
        self.author_id = author_id

    def __repr__(self):
        return '<TestSet %r>' % self.filename

    @cached_property
    def url(self):
        return testset.url(self.filename)

    @cached_property
    def permalink(self):
        return self._url(True)

    @cached_property
    def slug(self):
        return slugify(self.filename or '')[:80]


class TestBed(db.Model, dbFunctions):
    __tablename__ = "testbeds"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True)

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    __mapper_args__ = {'order_by' : id.desc()}


    # FIXME Test step
    def __init__(self, filename, author_id):
        self.filename = filename
        self.author_id = author_id

    def __repr__(self):
        return '<TestBed %r>' % self.filename

    @cached_property
    def url(self):
        return testbed.url(self.filename)


    @cached_property
    def permalink(self):
        return self._url(True)

    @cached_property
    def slug(self):
        return slugify(self.filename or '')[:80]


