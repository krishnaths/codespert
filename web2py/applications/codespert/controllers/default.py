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
import json 

@auth.requires_login()
def userlist():
    return dict()
    
@auth.requires_login()
def getuser():
##    tkMessageBox.showinfo("isassa")
    if(request.args(0) == "" or request.args(0) is None):
#        tkMessageBox.showinfo("i s")
        users = db().select(db.auth_user.ALL)
    else:
        strmatch = request.args(0)
##        tkMessageBox.showinfo("12324",strmatch)
        userlist = db().select(db.auth_user.ALL)
        users = userlist.find(lambda row:(row.first_name.lower().find(strmatch.lower()) != -1 or row.last_name.lower().find(strmatch.lower()) != -1))
    return dict(users=users)
    

@auth.requires_login()
def ajaxsearch():
    return dict()

    
@auth.requires_login()
def getqs():
    #tkMessageBox.showinfo('asdasd')
    questions = db().select(db.UsrQst.ALL)
    arrqs = []
    arrids = []
    for ques in questions:
#	tkMessageBox.showinfo(ques.question)
	arrqs.append(ques.question)
	arrids.append(ques.id)
    
    #data = json.loads(arrqs)
    #tkMessageBox.showinfo(data)
    return dict(arrqs=arrqs,arrids=arrids)
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

    var = mail.send('sankaran458@gmail.com', 'Hurray you have an answer!!!',Message)

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
            #tkMessageBox.showinfo(receiver+'sd')
            usrnm = db(db.auth_user.id == auth.user.id).select(db.auth_user.first_name)
            fname = ""
            for usr in usrnm:
                fname = usr.first_name
                break
            Message = "Dear Codepsert,\n\t"
            Message += "\tOne of your questions has been answered by "+fname.upper()+".Please click the link below to view the solution.\nhttp://127.0.0.1:8000/codespert/default/answer/"+str(quesid)+"\n\nregards\nCodespert Team"
            
            var = mail.send(receiver, 'Hurray you have an answer!!!',Message)
            
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
    
    qstion = db(db.UsrQst.id == request.args(0)).select(db.UsrQst.ALL)
    quest = ""
    tag = ""
    arrtags = []
    arrtagnames = []
    arrtagids = []
    for qst in qstion:
	#tkMessageBox.showinfo("hi"+qst.question)
	quest = qst.question
	tag = qst.tag
    arrtags = tag.split('|')
    for tak in arrtags:
	tagdets = db(db.Tags.id == tak).select(db.Tags.ALL)
	for tg in tagdets:
	    arrtagnames.append(tg.name)
	    arrtagids.append(tg.id)

	#    arrtagnames.append(tgname.name)
    #tkMessageBox.showinfo('tagnames'+str(arrtagnames))
	 
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
            #tkMessageBox.showinfo("inside post")        
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
        return dict(usrnm=auth.user.first_name.lower(),qid=request.args(0),qstion=quest,code=script,answers=answers,answerers=answerers,form=form,tagnames=arrtagnames,tagids=arrtagids)

def home():
    return dict()

@auth.requires_login()
def listqs():
    
    if request.vars['tid'] is None:
        quests = db().select(db.UsrQst.ALL)
	questions = []
	qids = []
	qtagids = []
	qtagnames = []
	qtags = []
	for qst in quests:
            questions.append(qst.question)
            qids.append(qst.id)
            qtags.append(qst.tag)
	for i in range(len(qtags)):
	    qtags[i] = qtags[i].split('|')

	for m in range(len(qtags)):
            qtagnames.append([])
            for k in range(len(qtags[m])):
                tgname = db(db.Tags.id == qtags[m][k]).select(db.Tags.name)
                for trname in tgname:
                    qtagnames[m].append(trname.name)
        return dict(quests=quests,qtagnames=qtagnames,qtagids=qtags,istid="0")
    else:
        
        tid = request.vars['tid']
        for qtagname in db(db.Tags.id == tid).select(db.Tags.name):
            qtagnames = qtagname.name
            
        #tkMessageBox.showinfo(str(type(request.vars['tid']))+"type")
        arrQids = []
        arrTids = []
        arrQues = []
        arrIds = []
        quests = db().select(db.UsrQst.ALL)
        
        for qst in quests:
            arrqTids = qst.tag.split('|')
            #tkMessageBox.showinfo(str(arrqTids)+"arrqTids")
            if tid in arrqTids:
                arrQids.append(qst.id)
        #tkMessageBox.showinfo(str(arrQids)+"arrqids")
        rows = quests.find(lambda row: row.id in arrQids)
        #for row in rows:
        #    tkMessageBox.showinfo(row.question)
        #    arrQues.append(row.question)
        #Now arrQids has all ids that has the selected tags
        return dict(quests=rows,qtagnames=qtagnames,qtagids=tid,istid="1")
            
        
        
     
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
    response.flash = T("Welcome to Codespert!")
    redirect(URL('static','codespert.html'))
    return dict()


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
