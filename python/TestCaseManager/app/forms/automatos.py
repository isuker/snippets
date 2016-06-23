# -*- coding: utf-8 -*- 
from flask.ext.wtf import Form, TextField, PasswordField, BooleanField,\
         SubmitField, validators, required, equal_to, file_required, \
         email, TextAreaField, HiddenField, RecaptchaField, regexp, \
         ValidationError, FileField, file_allowed, SelectField


################################################################################
#
# Form for Automatos
#
################################################################################
class UploadTestBedForm(Form):
    filename = FileField(u"Upload Test Bed")
    submit = SubmitField(u"Submit", id="upload_submit")

class UploadTestSetForm(Form):
    filename = FileField(u"Upload Test Set")
    submit = SubmitField(u"Submit", id="upload_submit")

class ExecuteForm(Form):
    testbed = SelectField("Choose Test Bed:", default=0, coerce=int)
    testset = SelectField("Choose Test Set:", default=0, coerce=int)
    testclient = SelectField("Choose Test Client:", default=0, coerce=int)
    submit = SubmitField()

