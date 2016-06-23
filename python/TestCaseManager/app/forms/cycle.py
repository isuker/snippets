# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, TextAreaField, RadioField, \
     SelectField, IntegerField, SubmitField, ValidationError, \
     optional, required, url

from app.models import Cycle
from app import db

class CycleForm(Form):
    name = TextField('Test Cycle Name:', validators=[
                      required(message="Name can't be None")], id = "cycle_name")
    build = TextField("Test Build:")
    description = TextAreaField(u"Test Cycle Description", id = "cycle_description")

    #tags = TextField("Separate by commma", id = "cycle_tags")
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        self.cycle = kwargs.get('obj', None)
        super(CycleForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        cycle = Cycle.query.filter(Cycle.name.like(field.data)).first()
        if cycle:
            raise ValidationError, "This test cycle has been existed" 

    def validate_link(self, field):
        cycles = Cycle.query.filter_by(link=field.data)
        if self.cycle:
            cycles = cycles.filter(db.not_(Cycle.id==self.cycle.id))
        if cycles.count():
            raise ValidationError, "This Test Link has been existed"

class CommentForm(Form):
    comment = TextAreaField(validators=[
                            required(message="内容不能为空")])
    submit = SubmitField(u"提交")
    cancel = SubmitField(u"取消")
