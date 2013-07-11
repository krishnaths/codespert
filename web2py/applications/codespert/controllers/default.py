# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from Tkinter import *
import tkMessageBox

def answer():
    qstion = db(db.UsrQst.id == 1).select(db.UsrQst.question)
    answers = db(db.Answer.qid == 1).select(db.Answer.answer)
    answerers = db(db.Answer.qid == 1)(db.Answer.byid == db.auth_user.id).select(db.Answer.answer,db.auth_user.first_name) 
#    tkMessageBox.showinfo("",answerers)
    codes = db(db.Codes.qid == 1).select(db.Codes.Code)
    
    for code in codes:
#	tkMessageBox.showinfo(code.Code)
	script = code.Code
    

    for answer in answers:
	pass
	#tkMessageBox.showinfo(answer.answer)
    for qst in qstion:
#	tkMessageBox.showinfo(qst.question)
        qstion = qst.question
    return dict(qstion=qst.question,code=script,answers=answers,answerers=answerers)

def home():
    return dict()

def listqs():
    quests = db(db.UsrQst.usrid == 1).select(db.UsrQst.ALL)
    questions = []
    for qst in quests:
        questions.append(qst.question)
    tkMessageBox.showinfo("hi",questions);        
    return dict(quests = questions)
     

def trainings():
    if request.args(0) == '' or request.args(0) == 'None':
	return dict(message='python')
    else :

	return dict(message=request.args(0))


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())