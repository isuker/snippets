from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from app.lib.util import DenormalizedText, dbFunctions, slugify,\
    tomarkdown, domain

from app.models import User,Case
from app import db

from datetime import datetime
from werkzeug import cached_property


class Result(db.Model, dbFunctions):
    __tablename__ = "results"

    PUBLIC = 100
    FRIENDS = 200
    PRIVATE = 300

    PASS = 10
    FAIL = 20
    BLOCK = 30
    NORUN = 40

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # automatos Test log link
    link = db.Column(db.String())
    # pass or fail
    status = db.Column(db.Integer)
    # fail at which loop
    loop = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    # each result map tp one test case
    case_id = db.Column(db.Integer,
                          db.ForeignKey(Case.id, ondelete='CASCADE'),
                          nullable=False)
    case = db.relation(Case, innerjoin=True, lazy="joined")

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    access = db.Column(db.Integer, default=PUBLIC)

    __mapper_args__ = {'order_by' : id.desc()}


    # FIXME Test step

    def __init__(self, *args, **kwargs):
        super(Result, self).__init__(*args, **kwargs)
        self.access = self.access or self.PUBLIC
        self.status = self.status or self.NORUN
        self.loop = 0

    def __repr__(self):
        return '<User %r>' % self.name

    def _url(self, _external=False):
        return url_for('result.view',
                       result_id=self.id,
                       slug=self.slug,
                       _external=_external)


    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)

    @cached_property
    def slug(self):
        return slugify(self.name or '')[:80]


