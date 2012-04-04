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
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
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
def song_form():
   form=SQLFORM.factory(db.Field('movie',db.movie,requires=IS_IN_DB(db,'movie.id','movie.name'),required=True,label='select movie'),
                        db.Field('singer',db.song,requires=IS_IN_DB(db,'song.id','song.singer'),required=True,label='select singer'))
   if form.accepts(request.vars,session):
      redirect(URL(r=request,f='songlist?movie=%d&singer=%d'%int(form.vars.movie,form.vars.singer)))
   elif form.errors:
      response.flash='Errors in form'
   return dict(form=form)
def songlist():
  movie=int(request.vars.movie)
  sing=int(request.vars.singer)
  ans=db((db.song.singer==sing) & (db.movie.id==movie)).select(db.song.name)
  return dict(f=ans)
           
def q_1():    
    rows=db((db.song.id ==db.artist.id) & (db.artist.id == 3)).select(db.song.name)    
    return dict(rows=rows)
def song_n_balu():    
    rows=db((db.song.singer == db.artist.id) & (db.artist.name == 'Balu')).select(db.song.ALL)

    return dict(rows=rows)
 
def singer_balu():    
    rows=db(((db.song.singer == db.artist.id) & (db.artist.name == 'Balu')) & ((db.song.movie == db.movie.id)& (db.movie.name=="Shankarabharanam"))).select(db.song.name)    
    return dict(rows=rows)
def earlier():    
    rows=db(((db.song.singer==db.artist.id) & (db.artist.singer=="Balu")) &  ((db.song.movie == db.movie.id)&(db.movie.release_date<'2000-01-01'))).select(db.song.name,db.artist.singing_actor)    
    return dict(rows=rows)
def show_song():
    form = SQLFORM(db.song)
    if form.accepts(request.vars,session):
       response.flash("DONE")
    elif form.errors:
       response.flash("ERROR")
    return dict(form=form)
