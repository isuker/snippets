# -*- coding: utf-8 -*
from flask import Blueprint, abort, jsonify, request,  \
    url_for, redirect, flash, render_template, current_app, \
    make_response
from flask.ext.login import current_user
from app.models import Case, TestSet, TestBed, TestJob
from app.forms import CommentForm, CaseForm, UploadTestBedForm, UploadTestSetForm, ExecuteForm
from app import db, mail, cache, testbed, testset
from app.lib.permissions import auth
from app.lib.worker import execute
from flask.ext.mail import Message
import setting
from datetime import datetime, timedelta
import time

#from flask.ext.uploads import save


mod = Blueprint('automatos', __name__)

result = None

################################################################################                                   
#                                                                                                                  
# Routine to Case view                                                                                             
#                                                                                                                  
################################################################################                                   


@mod.route("/add/<bed_or_set>", methods=['GET', 'POST'])
def add(bed_or_set):

    filename = None
    if bed_or_set == "TestBed":
        form = UploadTestBedForm()

        if request.method == "POST" and request.files['filename']:
            # save to local fs
            filename = testbed.save(request.files['filename'])
            # save to db
            tb = TestBed(filename,current_user.id) 
            tb.save()

            flash("Upload Test Bed success")
            return redirect(url_for('automatos.index'))

        return render_template("automatos/add_testbed.html", form=form)
    if bed_or_set == "TestSet":
        form = UploadTestSetForm()
        if request.method == "POST" and request.files['filename']:
            # save to local fs
            filename = testset.save(request.files['filename'])
            # save to db
            ts = TestSet(filename,current_user.id) 
            ts.save()

            flash("Upload Test Set success")
            return redirect(url_for('automatos.index'))
        return render_template("automatos/add_testset.html", form=form)

@mod.route("/view/<testType>/<int:id>")
def view(testType, id):

    if testType.upper() == "TESTBED":
        bed = TestBed.query.filter(TestBed.id==id).first_or_404()
        return render_template("automatos/testbed_detail.html", bed=bed)

    if testType.upper() == "TESTSET":
        set = TestSet.query.filter(TestSet.id==id).first_or_404()
        return render_template("automatos/testset_detail.html", set=set)


@mod.route("/delete/<testType>/<int:id>" ,methods=['POST'])
def delete(testType, id):

    if testType.upper() == "TESTBED":
        bed = TestBed.query.filter(TestBed.id==id).first_or_404()
        bed.delete()

    if testType.upper() == "TESTSET":
        set = TestSet.query.filter(TestSet.id==id).first_or_404()
        set.delete()

    return jsonify(success=True,
                   redirect_url=url_for('automatos.index')) 


@mod.route("/index", methods=['GET','POST'])
def index():
    beds = TestBed.query.all()
    sets = TestSet.query.all()

    form = ExecuteForm()
    form.testbed.choices = [(c.id, c.filename) for c in TestBed.query.all()]
    form.testset.choices = [(c.id, c.filename) for c in TestSet.query.all()]
    # TBD. we need support more test client
    form.testclient.choices = [(0, "ray's dev vm")]
    if form.validate_on_submit():

        # get TestBed and TestSet from user input
        testbed = TestBed.query.filter(TestBed.id==form.testbed.data).first()
        testset = TestSet.query.filter(TestSet.id==form.testset.data).first()

        # log this job
        job = TestJob(testbed, testset)
        job.author = current_user
        job.save()

        # start to execute Automatos
        logdir = "%s/job%s" %(current_user.username, job.id)
        result = execute.delay(testbed.id, testset.id, logdir)
        job.task_id = result.id
        job.status = TestJob.STARTED
        # sleep 2 second to wait for create test log
        time.sleep(1)
        job.link = "http://10.244.178.54/automatos/"+logdir
        job.save()

        flash("Start execute automatos")

        #return redirect(url_for("automatos.execute",jobID=job.id))
        return redirect(url_for("job.view", job_id=job.id))

    return render_template("automatos/index.html", beds=beds, sets=sets, form=form)

#@mod.route("/execute/<int:jobID>", methods=['GET', 'POST'])
#@mod.route("/execute", methods=['GET', 'POST'])
#def execute(jobID=None):
#    #job = TestJob.query.filter(TestJob.id==jobID).first_or_404()
#    #job.start()
#
#   #return render_template("automatos/execute.html", job=job)

