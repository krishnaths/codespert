from Tkinter import *
import tkMessageBox

# coding: utf8
# try something like
#def index(): return dict(message="hello from new.py")
def new():
    form=FORM(LABEL('Enter your question here',_class="traintext"),INPUT(_type='text',_name='txtQues',_id="txtQues",  requires=IS_NOT_EMPTY()),BR(),
              A('Detail your Question',_id="btnCode",_class="trainbtn"),BR(),BR(),
              LABEL('Please detail your question and add some code if u wud like to',_class="traintext",_id="lbldetail"),
              TEXTAREA(_name='txtCode',_id="code"),
              LABEL('Tags',_class="traintext"),BR(),INPUT(_name='tagname',_id="tag",requires=IS_NOT_EMPTY()),BR(),
              INPUT(_type='submit',_id="btnSubmit"))
    
    if form.process().accepted:
	arrtag = []
	arrtagids = []
	strtagids = ""
        Question = form.vars.txtQues
        Code = form.vars.txtCode
        #insert value into db for questions
        
        tags = form.vars.tagname
	tkMessageBox.showinfo("hi",tags)
        arrtag=tags.split(",")
        tkMessageBox.showinfo("hi2",arrtag)
	for i in arrtag:
            for row in db(db.Tags.name.lower() == i.lower()).select(db.Tags.id):
                arrtagids.append(row.id)
        for j in range(len(arrtagids)):
            if j == 0:
                strtagids = str(arrtagids[j])
            else:
                strtagids = str(strtagids)+"|"+str(arrtagids[j])
        if strtagids == "":
            response.flash = "Enter atleast one valid tag"
            tkMessageBox.showinfo("stringids",strtagids)
        else:
            #Now insert into db
            retqid = db.UsrQst.insert(question=Question,usrid=auth.user.id,tag=strtagids)
            tkMessageBox.showinfo("retqid",retqid.id)
            tkMessageBox.showinfo("retqid",form.vars.id)
            if Code != "":
                retcodeid = db.Codes.insert(qid=retqid,Code=Code)
            redirect(URL('../../default/answer/'+str(retqid.id))) 
                
        #redirect(URL('second'))
    return dict(form=form)

    
"""def first():
    form = FORM(INPUT(_name='visitor_name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        redirect(URL('second'))
    return dict(form=form)"""

def second():
    
    return dict()
