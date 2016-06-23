from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy


from app.lib.util import DenormalizedText, dbFunctions, slugify

from app.models import User, TestBed, TestSet
from app import db

from datetime import datetime
from werkzeug import cached_property


class TestJob(db.Model, dbFunctions):
    __tablename__ = "testjobs"

    # Job status
    STARTED = "Started"
    RUNNING = "Running"
    FINISHED = "Finishd"
    CANCELED = "Canceled"
    STOPPED = "Stopped"
    ERROR = "Error"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # celery task UUID
    task_id = db.Column(db.String)

    author_id = db.Column(db.Integer,
                          db.ForeignKey(User.id, ondelete='CASCADE'),
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")

    testbed_id = db.Column(db.Integer,
                          db.ForeignKey(TestBed.id, ondelete='CASCADE'),
                          nullable=False)
    testbed = db.relation(TestBed, innerjoin=True, lazy="joined")

    testset_id = db.Column(db.Integer,
                          db.ForeignKey(TestSet.id, ondelete='CASCADE'),
                          nullable=False)
    testset = db.relation(TestSet, innerjoin=True, lazy="joined")
 
    # whether job can be cancel or not
    cancelable = db.Column(db.Boolean, default=False)

    date_started = db.Column(db.DateTime, default=datetime.utcnow)
    date_finished = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    status = db.Column(db.String())
    link = db.Column(db.String())

    __mapper_args__ = {'order_by' : id.desc()}


    # FIXME Test step

    def __init__(self, testbed, testset):
        self.testbed = testbed
        self.testset = testset

    def __repr__(self):
        return '<TestJob %r>' % self.id

    def _url(self, _external=False):
        return url_for('job.view',
                       job_id=self.id,
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

