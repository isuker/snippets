# -*- coding: utf-8 -*
from flask import Blueprint, abort, jsonify, request,  \
    url_for, redirect, flash, render_template, current_app, \
    make_response
from flask.ext.login import current_user
from app.models import Cycle
from app.forms import CommentForm, CycleForm
from app import db, mail, cache
from app.lib.permissions import auth
from flask.ext.mail import Message
import setting
from datetime import datetime, timedelta



mod = Blueprint('cycle', __name__)

################################################################################                                   
#                                                                                                                  
# Routine to Cycle view                                                                                             
#                                                                                                                  
################################################################################                                   


@mod.route("/add", methods=['GET','POST'])
#@auth.require(401)
def add():
    form = CycleForm()
    if form.validate_on_submit():

        cycle = Cycle()
        form.populate_obj(cycle)
        cycle.author = current_user
        cycle.save()
        flash("Add Test Cycle successfully")
        return redirect(url_for("cycle.view", cycle_id=cycle.id))
    return render_template("cycle/add.html", form=form)

@mod.route("/index")
def index():
    cycles = Cycle.query.all()
    return render_template("cycle/index.html" ,cycles=cycles)

@mod.route("/<int:cycle_id>/")                                                                                      
@mod.route("/<int:cycle_id>/s/<slug>/")                                                                             
#@keep_login_url                                                                                                   
def view(cycle_id, slug=None):                                                                                      
    cycle = Cycle.query.get_or_404(cycle_id)                                                                          
    #if not cycle.permissions.view:                                                                                  
    #    if not current_user:                                                                                       
    #        flash(u"你需要先登录", "error")                                                                        
    #        return redirect(url_for("account.login", next=request.path))                                           
    #    else:                                                                                                      
    #        flash(u"你需要有权限", "error")                                                                        
    #        abort(403)                                                                                             
                                                                                                                   
    def edit_comment_form(comment):                                                                                
        return CommentForm(obj=comment)                                                                            
                                                                                                                   
    return render_template("cycle/cycle.html",                                                                       
                           #comment_form=CommentForm(),                                                             
                           #edit_comment_form=edit_comment_form,                                                    
                           cycle=cycle)

@mod.route("/<int:cycle_id>/edit/", methods=['GET', 'POST'])                                                        
#@auth.require(401)                                                                                                 
def edit(cycle_id):
    cycle = Cycle.query.get_or_404(cycle_id)                                                                          
    #cycle.permissions.edit.test(403)                                                                                
    form = CycleForm(obj=cycle)
    if form.validate_on_submit():                                                                                  
        form.populate_obj(cycle)                                                                                    
        cycle.save()
        flash(u"你的条目已更新", "successfully")
        return redirect(url_for("cycle.view", cycle_id=cycle_id))                                                     
    return render_template("cycle/edit_cycle.html",                                                                  
                           cycle=cycle,                                                                              
                           form=form)                                                                              
                                                                                                                   

@mod.route("/<int:cycle_id>/delete/", methods=("POST",))                                                            
#@auth.require(401)
def delete(cycle_id):
    cycle = Cycle.query.get_or_404(cycle_id)                                                                          
    #cycle.permissions.delete.test(403)                                                                              
    cycle.delete()
    #if current_user.id != cycle.author_id:                                                                          
    #    if setting.MAIL_ENABLE: 
    #        body = render_template("emails/cycledeleted.html",                                                      
    #                               cycle=cycle)
    #        message = Message(subject=u"你提交的条目已删除",                                                       
    #                          body=body,
    #                          recipients=[cycle.author.email])                                                      
    #        
    #        mail.send(message)
    #        flash(u"条目已被删除", "successfully")                                                                 
    #    else:
    #        flash(u"邮件服务器未开启，请联系管理员", "error")                                                      
    #else:
    #    flash(u"你的条目成功删除", "successfully")                                                                 
    return jsonify(success=True,
                   redirect_url=url_for('cycle.index')) 
