# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, TextAreaField, RadioField, \
     SelectField, IntegerField, SubmitField, ValidationError, \
     optional, required, url

from app.models import Result
from app import db

class ResultForm(Form):
    name = TextField('Test Result Name:', validators=[
                      required(message="Name can't be None")], id = "result_name")
    case = SelectField("Test Case:", default=0, coerce=int)

    link = TextField("Test Log Link:", default="http://", validators=[
                     optional(),
                     url(message="Must be valid link")], id = "case_link")

    loop = IntegerField("Test loop:", validators=[optional()])

    status = SelectField("Test Result:", default=Result.PASS, coerce=int,
                       choices=[(Result.PASS, "Pass"),
                                (Result.FAIL, "Fail"),
                                (Result.BLOCK, "Blocked"),
                                (Result.NORUN, "No Run")])

    #tags = TextField("Separate by commma", id = "result_tags")
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        self.result = kwargs.get('obj', None)
        super(ResultForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        result = Result.query.filter(Result.name.like(field.data)).first()
        if result:
            raise ValidationError, "This test result has been existed" 

    def validate_link(self, field):
        results = Result.query.filter(Result.access==Result.PUBLIC).filter_by(link=field.data)
        if self.result:
            results = results.filter(db.not_(Result.id==self.result.id))
        if results.count():
            raise ValidationError, "This Test Link has been existed"

class CommentForm(Form):
    comment = TextAreaField(validators=[
                            required(message="内容不能为空")])
    submit = SubmitField(u"提交")
    cancel = SubmitField(u"取消")
