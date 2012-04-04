# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
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
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


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
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
def q2f():
  form = SQLFORM.factory(db.Field('namen',db.artist,requires=IS_IN_DB(db,'artist.id','artist.artist_name'),label='Select artist name'))
  if form.accepts(request.vars,session):
    redirect(URL(r=request, f='q2s?namen='+form.vars.namen))
  elif form.errors:
    response.flash='Errors in form Please re-enter'
  return dict(form=form)  
def q2s():
  sname=str(request.vars.namen)
  #here whatever be always sname will be referred by id ! 
  rows=db(db.song.singer==sname).select(db.song.name,db.song.id)
  return dict(rows=rows)
def q3f():
  form = SQLFORM.factory(db.Field('namen',db.artist,requires=IS_IN_DB(db,'artist.id','artist.artist_name'),label='Select Artist'),
                         db.Field('movien',db.movie,requires=IS_IN_DB(db,'movie.id','movie.name'),label='Select movie'))
  if form.accepts(request.vars,session):
    redirect(URL(r=request, f='q3s?namen='+form.vars.namen+'&movien='+form.vars.movien))
  elif form.errors:
    response.flash='Errors in form Please re-enter'
  return dict(form=form)                         
def q3s():
  sname=str(request.vars.namen)
  movien=str(request.vars.movien)
  rows=db((db.song.singer==sname) & (db.song.movie==movien)).select(db.song.name,db.song.id)
  return dict(rows=rows)
def q4f():
  form = SQLFORM.factory(db.Field('movien',db.movie,requires=IS_IN_DB(db,'movie.id','movie.name'),label='Select movie'))
  if form.accepts(request.vars,session):
    redirect(URL(r=request, f='q4s?&movien='+form.vars.movien))
  elif form.errors:
    response.flash='Errors in form Please re-enter'
  return dict(form=form) 
def q4s():
  movien=str(request.vars.movien)
  rows=db(db.song.movie==movien).select(db.song.name,db.song.id)
  return dict(rows=rows)
def insong():
  form = SQLFORM(db.song)
  if form.accepts(request.vars,session):
      #redirect(URL(r=request, f='student_details?rollno=%d' % form.vars.rollno))
      response.flash='New Song Record Inserted'
  elif form.errors:
      response.flash='Errors in form'
  return dict(form=form)
def newq():
  return dict()
def song_details():
  idn=int(request.vars.id)
  records=db(db.song.id==idn).select(db.song.ALL)
  return dict(records=records)
