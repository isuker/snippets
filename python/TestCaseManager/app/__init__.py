# -*- coding: utf-8 -*- 
from flask import Flask, render_template, request, jsonify, \
    redirect, url_for, flash, make_response
from flask.ext.cache import Cache 
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, DATA, TEXT, configure_uploads
from flask.ext.principal import Principal,identity_loaded,AnonymousIdentity
import setting

import sys

app = Flask(__name__)
app.config.from_object(setting)


db = SQLAlchemy(app)
# http://stackoverflow.com/questions/20201809/sqlalchemy-flask-attributeerror-session-object-has-no-attribute-model-chan
# http://flask.pocoo.org/docs/patterns/sqlalchemy/
#db.session._model_changes={}


app.debug = True
#toolbar = DebugToolbarExtension(app)

mail = Mail(app)
babel = Babel(app)
cache = Cache(app)


principals = Principal(app)
login_manager = LoginManager()
login_manager.setup_app(app)
testbed = UploadSet('TestBed', DATA)
testset = UploadSet('TestSet', DATA)
configure_uploads(app, (testset,testbed))

# setting
# fix issue of unicode
reload(sys)
sys.setdefaultencoding("utf-8")

################################################################
#
# add filters for template
#
################################################################
from app.lib.util import timesince, basename, torst, tomarkdown
app.jinja_env.filters['timesince'] = timesince
app.jinja_env.filters['basename'] = basename
app.jinja_env.filters['rst'] = torst
app.jinja_env.filters['markdown'] = tomarkdown

################################################################
#
# add basic routes
#
################################################################
from blinker import Namespace
signals = Namespace()

comment_added = signals.signal("comment-added")
comment_deleted = signals.signal("comment-deleted")


@comment_added.connect
def comment_added(case):
    case.num_comments += 1
  
################################################################
#
# add basic setup
#
################################################################
from app.models import User

@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except:
        return None

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # find the role for user
    try:
        identity.provides = User.query.filter(User.username.like(identity.name)).first().provides
    except:
        identity = AnonymousIdentity


#############################
from view import home
from view import case
from view import account
from view import user 
from view import comment
from view import result
from view import cycle
from view import automatos
from view import job


app.register_blueprint(home.mod)
app.register_blueprint(case.mod, url_prefix='/case')
app.register_blueprint(cycle.mod, url_prefix='/cycle')
app.register_blueprint(account.mod, url_prefix='/account')
app.register_blueprint(user.mod, url_prefix='/user')
app.register_blueprint(comment.mod, url_prefix='/comment')
app.register_blueprint(result.mod, url_prefix='/result')
app.register_blueprint(automatos.mod, url_prefix='/automatos')
app.register_blueprint(job.mod, url_prefix='/job')
