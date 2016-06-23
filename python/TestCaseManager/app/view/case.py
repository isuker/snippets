# -*- coding: utf-8 -*
from flask import Blueprint, abort, jsonify, request,  \
    url_for, redirect, flash, render_template, current_app, \
    make_response
from flask.ext.login import current_user
from app.models import Case
from app.forms import CommentForm, CaseForm
from app import db, mail, cache
from app.lib.permissions import auth
from flask.ext.mail import Message
import setting
from datetime import datetime, timedelta



mod = Blueprint('case', __name__)

################################################################################                                   
#                                                                                                                  
# Routine to Case view                                                                                             
#                                                                                                                  
################################################################################                                   


@mod.route("/add", methods=['GET','POST'])
#@auth.require(401)
def add():
    form = CaseForm()
    if form.validate_on_submit():

        case = Case(name=form.name)
        form.populate_obj(case)
        case.author = current_user
        case.save()
        flash("Add Test Case successfully")
        return redirect(url_for("case.view", case_id=case.id))
    return render_template("case/add.html", form=form)

@mod.route("/index")
def index():
    cases = Case.query.all()
    return render_template("case/index.html" ,cases=cases)

@mod.route("/<int:case_id>/")                                                                                      
@mod.route("/<int:case_id>/s/<slug>/")                                                                             
#@keep_login_url                                                                                                   
def view(case_id, slug=None):                                                                                      
    case = Case.query.get_or_404(case_id)                                                                          
    #if not case.permissions.view:                                                                                  
    #    if not current_user:                                                                                       
    #        flash(u"你需要先登录", "error")                                                                        
    #        return redirect(url_for("account.login", next=request.path))                                           
    #    else:                                                                                                      
    #        flash(u"你需要有权限", "error")                                                                        
    #        abort(403)                                                                                             
                                                                                                                   
    def edit_comment_form(comment):                                                                                
        return CommentForm(obj=comment)                                                                            
                                                                                                                   
    return render_template("case/case.html",                                                                       
                           #comment_form=CommentForm(),                                                             
                           #edit_comment_form=edit_comment_form,                                                    
                           case=case)

@mod.route("/<int:case_id>/edit/", methods=['GET', 'POST'])                                                        
#@auth.require(401)                                                                                                 
def edit(case_id):
    case = Case.query.get_or_404(case_id)                                                                          
    #case.permissions.edit.test(403)                                                                                
    form = CaseForm(obj=case)
    if form.validate_on_submit():                                                                                  
        form.populate_obj(case)                                                                                    
        case.save()
        flash(u"你的条目已更新", "successfully")
        return redirect(url_for("case.view", case_id=case_id))                                                     
    return render_template("case/edit_case.html",                                                                  
                           case=case,                                                                              
                           form=form)                                                                              
                                                                                                                   

@mod.route("/<int:case_id>/delete/", methods=("POST",))                                                            
#@auth.require(401)
def delete(case_id):
    case = Case.query.get_or_404(case_id)                                                                          
    #case.permissions.delete.test(403)                                                                              
    case.delete()
    #if current_user.id != case.author_id:                                                                          
    #    if setting.MAIL_ENABLE: 
    #        body = render_template("emails/casedeleted.html",                                                      
    #                               case=case)
    #        message = Message(subject=u"你提交的条目已删除",                                                       
    #                          body=body,
    #                          recipients=[case.author.email])                                                      
    #        
    #        mail.send(message)
    #        flash(u"条目已被删除", "successfully")                                                                 
    #    else:
    #        flash(u"邮件服务器未开启，请联系管理员", "error")                                                      
    #else:
    #    flash(u"你的条目成功删除", "successfully")                                                                 
    return jsonify(success=True,
                   redirect_url=url_for('case.index')) 
