# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from gluon.tools import Mail
from Tkinter import *
import tkMessageBox
import logging

@auth.requires_login()
def getqs():
#    tkMessageBox.showinfo('asdasd')
    questions = db().select(db.UsrQst.question)
    arrqs = []
    for ques in questions:
#	tkMessageBox.showinfo(ques.question)
	arrqs.append(ques.question)
    #arrqs = [{"value":"Hello"},{"value":"Hi Mother"},{"value" : "This is probable"},{"value":"This is also called as suggestion"}]
    return response.json(arrqs)
    #return dict(value=arrqs)


@auth.requires_login()
def searchqs_bk():
    return dict(hi="hello",value="sad")

@auth.requires_login()
def searchqs():
    return dict(hi="hello",value="sad")

@auth.requires_login()
def mailit(qid):
    mail = Mail()
    mail.settings.server = 'smtp.gmail.com:587'
    mail.settings.sender = 'evtmng@gmail.com'
    mail.settings.tls = True
    mail.settings.login = 'evtmng@gmail.com:th1s1smypass'
    usrnm = db(db.auth_user.id == auth.user.id).select(db.auth_user.first_name) 
    Message = "One of your questions has been answered by "+usrnm 
    #.Please click the link below.\nhttp://127.0.0.1:8000/codespert/default/answer/"+str(qid)"+\n\nregards\nCodespert Team"

    var = mail.send('sankaran458@gmail.com', 'hello',Message)

    if var == 1:

        #redirect(URL('invite?eid='+evnt_Id))
        #response.flash = T("Invitation mail sent successfully")
        #session.flash = T("Invitation")
        pass
    else:
        response.flash = "We are facing some issues.We are working on it"
    return var

@auth.requires_login()
def insertanswer():
    try:
        
        ans = request.body.read()
        ans = ans.replace('/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g', '<br />')
        quesid = request.args(0)
        
        ret = db.Answer.insert(qid=quesid,answer=ans,byid=auth.user.id)
	
	
        if ret >=1 :
            mail = Mail()
            mail.settings.server = 'smtp.gmail.com:587'
            mail.settings.sender = 'evtmng@gmail.com'
            mail.settings.tls = True
            mail.settings.login = 'evtmng@gmail.com:th1s1smypass'
            receiver = ""
            receivers = db(db.UsrQst.id == quesid)(db.UsrQst.usrid == db.auth_user.id).select(db.auth_user.email)
            for rec in receivers:
                receiver = rec.email
                break
            tkMessageBox.showinfo(receiver+'sd')
            usrnm = db(db.auth_user.id == auth.user.id).select(db.auth_user.first_name)
            fname = ""
            for usr in usrnm:
                fname = usr.first_name
                break
            Message = "Dear Codepsert,\n\t"
            Message += "One of your questions has been answered by "+fname.upper()+".Please click the link below.\nhttp://127.0.0.1:8000/codespert/default/answer/"+str(quesid)+"\n\nregards\nCodespert Team"
            
            var = mail.send(receiver, 'hello',Message)
            
            response.flash = "created post"
            return True
        else:
            response.flash = "An error occured while creating the post"
            return False
            
    except ValueError:
            pass
    return True

@auth.requires_login()
def answer():
    
    qstion = db(db.UsrQst.id == request.args(0)).select(db.UsrQst.question)
    quest = ""
    for qst in qstion:
	#tkMessageBox.showinfo("hi"+qst.question)
	quest = qst.question
    answers = db(db.Answer.qid == request.args(0)).select(db.Answer.answer)
    answerers = db(db.Answer.qid == request.args(0))(db.Answer.byid == db.auth_user.id).select(db.Answer.answer,db.auth_user.first_name) 
    codes = db(db.Codes.qid == request.args(0)).select(db.Codes.Code)
    script=""
    qst=[]
    for code in codes:
	script = code.Code
    #tkMessageBox.showinfo(codes)

    for answer in answers:
	#tkMessageBox.showinfo(answer)

	pass

    form=FORM(TEXTAREA(_id="txtAnswers",_placeholder="Your solution here",_name="txtAns",requires=IS_NOT_EMPTY()),BR(),INPUT(_type="submit",_id="btnsubmit",_value="Post"))
    form['_id'] = "frmAnswer"
    
    if form.accepts(request,session):
	try:
            tkMessageBox.showinfo("inside post")        
            valText = form.vars.txtAns.replace('/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g', '<br />')
            
            ret = db.Answer.insert(qid=request.args(0),answer=valText,byid=auth.user.id)
            if ret >=1 :
                response.flash = "An error occured while creating the post"
                return True
                pass
            else:
                response.flash = "An error occured while creating the post"
                return False
            
        except ValueError:
            pass
        
	   
	
    if qst ==  "":
        return dict(qstion="")
    else:
        return dict(usrnm=auth.user.first_name.lower(),qid=request.args(0),qstion=quest,code=script,answers=answers,answerers=answerers,form=form)

def home():
    return dict()

@auth.requires_login()
def listqs():
    #quests = db(db.UsrQst.usrid == 1).select(db.UsrQst.ALL)
    quests = db().select(db.UsrQst.ALL)
    questions = []
    qids = []
    for qst in quests:
        questions.append(qst.question)
	qids.append(qst.id)
    #return dict(quests = questions,qids=qids)
    return dict(quests=quests)
     
@auth.requires_login()
def trainings():
    if request.args(0) == '' or request.args(0) == 'None':
	return dict(message='python')
    else :

	return dict(message=request.args(0))

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    redirect(URL('static','codespert.html'))
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
