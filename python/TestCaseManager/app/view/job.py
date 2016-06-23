# -*- coding: utf-8 -*
from flask import Blueprint, abort, jsonify, request,  \
    url_for, redirect, flash, render_template, current_app, \
    make_response
from flask.ext.login import current_user
from app.models import TestJob, Case
from app.forms import CommentForm
from app import db, mail, cache
from app.lib.permissions import auth
from flask.ext.mail import Message
import setting
from datetime import datetime, timedelta

from app.lib.worker import query,stop
import celery


mod = Blueprint('job', __name__)

################################################################################                                   
#                                                                                                                  
# Routine to TestJob view                                                                                             
#                                                                                                                  
################################################################################                                   
@mod.route("/")
@mod.route("/index")
def index():
    jobs = TestJob.query.all()
    return render_template("job/index.html" ,jobs=jobs)

@mod.route("/<int:job_id>/")                                                                                      
#@keep_login_url                                                                                                   
def view(job_id):                                                                                      
    job = TestJob.query.get_or_404(job_id) 

    #ayncResult = query(job_id)
    status, response = query(job_id)
    #asyncResult = query.delay(job_id)
    #status, response = asyncResult.get()
    
    # map status from celery task to TestJob
    if status == celery.states.SUCCESS:
        job.status = TestJob.FINISHED
    elif status == celery.states.STARTED:
        job.status = TestJob.STARTED
    elif status == celery.states.FAILURE:
        job.status = TestJob.ERROR
    elif status == celery.states.PENDING:
        job.status = TestJob.RUNNING
    elif status == celery.states.REVOKED:
        job.status = TestJob.CANCELED
    else:
        job.status = status
    job.save()

    # convert to unicode
    output = map(lambda line: line.decode(), response['stdout'])
    
    return render_template("job/job.html", job=job, output=output)

@mod.route("<int:job_id>", methods=['POST'])
def cancel(job_id):

    job = TestJob.query.get_or_404(job_id)
    if job.status == TestJob.RUNNING:
        stop(job_id)
        job.status = TestJob.CANCELED
        job.save()
        return redirect(url_for("job.index"))
    else:
        output = ['This job is not running, it does not make sense to cancel it.']
        return render_template("job/job.html", job=job, output=output)


@mod.route("/<int:job_id>/delete/", methods=("POST",))                                                            
#@auth.require(401)
def delete(job_id):
    job = TestJob.query.get_or_404(job_id)                                                                          
    job.delete()
    return jsonify(success=True,
                   redirect_url=url_for('job.index')) 
