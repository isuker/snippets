from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from app.lib.util import DenormalizedText, dbFunctions, slugify,\
    tomarkdown, domain

from app.models import User
from app import db

from datetime import datetime
from werkzeug import cached_property


class Cycle(db.Model, dbFunctions):
    __tablename__ = "cycles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    build = db.Column(db.String())
    description = db.Column(db.String())

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    __mapper_args__ = {'order_by' : id.desc()}


    # FIXME Test step

    def __init__(self, *args, **kwargs):
        super(Cycle, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.name

    def _url(self, _external=False):
        return url_for('cycle.view',
                       cycle_id=self.id,
                       slug=self.slug,
                       _external=_external)


    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)

    @cached_property
    def markdown(self):
        return tomarkdown(self.description or '')

    @cached_property
    def slug(self):
        return slugify(self.name or '')[:80]


