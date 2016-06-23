# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, TextAreaField, RadioField, \
        SubmitField, ValidationError, optional, required, url

from app.models import Case
from app import db

class CaseForm(Form):
    name = TextField('Test Case Name', validators=[
                      required(message="Test Name can't be None")], id = "case_name")

    description = TextAreaField(u"Test Description", id = "case_description")
    #tags = TextField("Separate by commma", id = "case_tags")
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        self.case = kwargs.get('obj', None)
        super(CaseForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        case = Case.query.filter(Case.name.like(field.data)).first()
        if case:
            raise ValidationError, "This test case has been existed" 

    def validate_link(self, field):
        cases = Case.query.public().filter_by(link=field.data)
        if self.case:
            cases = cases.filter(db.not_(Case.id==self.case.id))
        if cases.count():
            raise ValidationError, u"这个链接已经有人提交了"

class CommentForm(Form):
    comment = TextAreaField(validators=[
                            required(message="内容不能为空")])
    submit = SubmitField(u"提交")
    cancel = SubmitField(u"取消")
