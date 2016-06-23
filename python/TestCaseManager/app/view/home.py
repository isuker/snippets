# -*- coding: utf-8 -*- 
from flask import Blueprint, render_template, url_for,\
    flash, g, redirect, request, abort, jsonify
from flask.ext.login import current_user
from flask.ext.mail import Message
from app.lib.permissions import auth
from app.lib.util import tomarkdown
from feedparser import parse
from urlparse import urlparse
import setting
import re

from app.models import Case, Result, Cycle
from app.models import TestBed, TestSet


"""
    定义home模块，在app.__init__.py中加载
"""
mod = Blueprint('home', __name__)

################################################################################
#
# Routine to Home view
#
################################################################################
@mod.route("/")
@mod.route('/index')
def index():
    return render_template("home/index.html")

@mod.route("/case")
def case():
    cases = Case.query.all()
    return render_template("case/index.html" ,cases=cases)

@mod.route("/cycle")
def cycle():
    cycles = Cycle.query.all()
    return render_template("cycle/index.html", cycles=cycles)

@mod.route("/result")
def result():
    results = Result.query.all()
    return render_template("result/index.html", results=results)

@mod.route("/automatos")
def automatos():
    return redirect(url_for("automatos.index"))

@mod.route("/help")
def help():
    return "TBD. Help doc here"

@mod.route("/about")
def about():
    words = open("README.md").read()
    return render_template("home/about.html", words=words)
