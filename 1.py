def first():
#  form=SQLFORM.factory(db.Field('id',db.artist,requires=IS_IN_DB(db,'artist.id'),required=True,label='Select Singer id'))#  form=SQLFORM(db.query) #form=FORM(INPUT(_name='singer',requires=IS_NOT_EMPTY()),INPUT(_type='submit')) #
  form = SQLFORM.factory(db.Field('id',db.artist,requires=IS_IN_DB(db,'artist.id','artist.id'),label='Select id'))
  if form.accepts(request.vars,session):
    redirect(URL(r=request, f='second?id=%d' % form.vars.id))
  elif form.errors:
    response.flash='Errors in form'
  return dict(form=form)  
  #return dict()
def second():
  sname = int(request.vars.id)
  rows=db(db.artist.id==sname).select(db.artist.artist_name)
  snames=str(rows[0].artist_name)
  rows1=db(db.song.singer==snames).select(db.song.name)
  return dict(rows1=rows1)
