# -*- coding: utf-8 -*
from flask import Blueprint, abort, jsonify, request,  \
    url_for, redirect, flash, render_template, current_app, \
    make_response
from flask.ext.login import current_user
from app.models import Result, Case
from app.forms import CommentForm, ResultForm
from app import db, mail, cache
from app.lib.permissions import auth
from flask.ext.mail import Message
import setting
from datetime import datetime, timedelta



mod = Blueprint('result', __name__)

################################################################################                                   
#                                                                                                                  
# Routine to Result view                                                                                             
#                                                                                                                  
################################################################################                                   


@mod.route("/add", methods=['GET','POST'])
#@auth.require(401)
def add():
    form = ResultForm()
    form.case.choices = [(c.id, c.name) for c in Case.query.all()]
    if form.validate_on_submit():

        result = Result()
        form.populate_obj(result)
        result.case = Case.query.filter(Case.id==form.case.data).first_or_404()
        result.author = current_user
        result.save()
        flash("Add Test Result successfully")
        return redirect(url_for("result.view", result_id=result.id))
    return render_template("result/add.html", form=form)

@mod.route("/index")
def index():
    results = Result.query.all()
    return render_template("result/index.html" ,results=results)

@mod.route("/<int:result_id>/")                                                                                      
@mod.route("/<int:result_id>/s/<slug>/")                                                                             
#@keep_login_url                                                                                                   
def view(result_id, slug=None):                                                                                      
    result = Result.query.get_or_404(result_id)                                                                          
    #if not result.permissions.view:                                                                                  
    #    if not current_user:                                                                                       
    #        flash(u"你需要先登录", "error")                                                                        
    #        return redirect(url_for("account.login", next=request.path))                                           
    #    else:                                                                                                      
    #        flash(u"你需要有权限", "error")                                                                        
    #        abort(403)                                                                                             
                                                                                                                   
    def edit_comment_form(comment):                                                                                
        return CommentForm(obj=comment)                                                                            

    return render_template("result/result.html",                                                                       
                           #comment_form=CommentForm(),                                                             
                           #edit_comment_form=edit_comment_form,                                           
                           result=result)

@mod.route("/<int:result_id>/edit/", methods=['GET', 'POST'])                                                        
#@auth.require(401)                                                                                                 
def edit(result_id):
    result = Result.query.get_or_404(result_id)                                                                          
    #result.permissions.edit.test(403)                                                                                
    form = ResultForm(obj=result)
    if form.validate_on_submit():                                                                                  
        form.populate_obj(result)                                                                                    
        result.save()
        flash(u"你的条目已更新", "successfully")
        return redirect(url_for("result.view", result_id=result_id))                                                     
    return render_template("result/edit_result.html",                                                                  
                           result=result,                                                                              
                           form=form)                                                                              
                                                                                                                   

@mod.route("/<int:result_id>/delete/", methods=("POST",))                                                            
#@auth.require(401)
def delete(result_id):
    result = Result.query.get_or_404(result_id)                                                                          
    #result.permissions.delete.test(403)                                                                              
    result.delete()
    #if current_user.id != result.author_id:                                                                          
    #    if setting.MAIL_ENABLE: 
    #        body = render_template("emails/resultdeleted.html",                                                      
    #                               result=result)
    #        message = Message(subject=u"你提交的条目已删除",                                                       
    #                          body=body,
    #                          recipients=[result.author.email])                                                      
    #        
    #        mail.send(message)
    #        flash(u"条目已被删除", "successfully")                                                                 
    #    else:
    #        flash(u"邮件服务器未开启，请联系管理员", "error")                                                      
    #else:
    #    flash(u"你的条目成功删除", "successfully")                                                                 
    return jsonify(success=True,
                   redirect_url=url_for('result.index')) 
