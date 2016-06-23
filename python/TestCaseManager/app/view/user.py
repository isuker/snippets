# -*- coding: utf-8 -*- 
from flask import Blueprint, render_template, jsonify,\
    url_for, g, redirect, flash, request
from werkzeug import secure_filename
from flask.ext.login import current_user
from app.forms import MessageForm, SearchUserForm
#UploadImageForm
from app.models import Case, User, Comment, TestJob
# UserImage, Action
from app.lib.permissions import auth
from app import db
import Image
import time, os
import setting


mod = Blueprint('user', __name__)

################################################################################
#
# Routine to User view
#
################################################################################
@mod.route("/" , methods=['GET', 'POST'])
@mod.route("/index/", methods=['GET', 'POST'])
#@cached()
#@keep_login_url
def index():
    form = SearchUserForm()
    users = User.query.random(10)
    if form.validate_on_submit():
        users = User.query.filter(User.username.like(form.search.data)).all()
    return render_template("user/index.html",
                           users=users, form=form)


@mod.route("/<username>/")
def home(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user/home.html", user=user)

@mod.route("/<username>/job")
#@cached()
#@auth.require(401)
def jobs(username):
    user = User.query.filter_by(username=username).first_or_404()
    #page_obj = Case.query.filter_by(author=user).as_list().paginate(page, Case.PER_PAGE)
    #page_url = lambda page: url_for('user.cases',
    #                                username=username,
    #                                page=page)

    #num_comments = Comment.query.filter_by(author_id=user.id).count()
    jobs = TestJob.query.filter(TestJob.author_id == user.id).all()

    return render_template("user/jobs.html",
                           user=user, jobs=jobs)
    #                       num_cases=page_obj.total,
    #                       num_comments=num_comments,
    #                       page_obj=page_obj,
    #                       page_url=page_url)


@mod.route("/<username>/comments/")
@mod.route("/<username>/comments/<int:page>/")
#@cached()
@auth.require(401)
def comments(username, page=1):
    user = User.query.filter_by(username=username).first_or_404()
    page_obj = Comment.query.filter_by(author=user).\
        order_by(Comment.id.desc()).restricted(current_user).\
        paginate(page, Comment.PER_PAGE)
    
    page_url = lambda page: url_for('user.comments',
                                    username=username,
                                    page=page)

    num_cases = Case.query.filter_by(author_id=user.id).\
        restricted(current_user).count()

    return render_template("user/comments.html",
                           user=user,
                           num_cases=num_cases,
                           num_comments=page_obj.total,
                           page_obj=page_obj,
                           page_url=page_url)



@mod.route("/mail/<int:user_id>/", methods=['GET', 'POST'])
@auth.require(401)
def send_mail(user_id):
    user = User.query.get_or_404(user_id)
    #user.permissions.send_message.test(403)
    form = MessageForm()
    if form.validate_on_submit():
        if setting.MAIL_ENABLE:
            body = render_template("emails/send_message.html",
                                   user=user,
                                   subject=form.subject.data,
                                   message=form.message.data)
            subject ="邮件来自 %s" % current_user.username
            message = Message(subject=subject,
                              body=body,
                              recipients=[user.email])
            mail.send(message)
            flash(u"给%s的邮件已发出" % user.username, "successfully")
        else:
            flash(u"邮件服务器未开启，请联系管理员", "error")
        return redirect(url_for("user.cases", username=user.username))
    return render_template("user/send_mail.html", user=user, form=form)

@mod.route("/<username>/image/", methods=['GET', 'POST'])
@auth.require(401)
def uploadimage(username):
    form = UploadImageForm(request.form)
    user = User.query.filter(User.username==username).first()
    image_url = None
    filename = None
    if request.method == 'POST' and request.files['image']:
        # save image
        filename = userimage.save(request.files['image'], name=current_user.username + '.jpg')
        image_url = userimage.url(filename)
        flash(u"%s 已上传"% filename, 'successfully')
        return render_template("user/uploadimage.html", form=form, user=user, image_url = image_url)
    else:
        return render_template("user/uploadimage.html", form=form, user=user, image_url = image_url)
    

@mod.route("/<username>/camera/", methods=['GET', 'POST'])
@auth.require(401)
def camera(username):
    basename = username + ".jpg"
    target_folder = setting.AVATAR_PATH
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target = os.path.join(target_folder, basename)
    f = open(target, 'wb')
    f.write(request.data)
    f.close()
    ret = {'status' : 1,
           'statusText' : u'上传成功!',
           'large': "test",
           'data' : {
                'photoId' : username,
                'urls' : ["avatar/" + username + ".jpg"]
                }
           }
    return jsonify(ret)


@mod.route("/saveavatar/", methods=['GET', 'POST'])
@auth.require(401)
def saveavatar():
    type = 'small'
    if request.args.get('type'):
        type = request.args.get('type')
    picid = request.args.get('photoId')
    basename =  str(picid) +  '_' +str(type) + '.jpg'
    target_folder = setting.AVATAR_PATH
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target = os.path.join(target_folder, basename)
    f = open(target, 'wb')
    f.write(request.data)
    f.close()
    ret = {'status' : 1,
           'statusText' : u'上传成功!',
           'large': "test",
           'data' : {
                'photoId' : picid,
                'urls' : ["test"]
                }
           }
    return jsonify(ret)

