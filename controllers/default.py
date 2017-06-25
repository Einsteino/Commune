# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from gluon.contrib.user_agent_parser import mobilize
from gluon.tools import geocode

def index():
    stuff = db(db.aevent).select()
    return locals()

def createEvent():
    form = SQLFORM(db.aevent)
    address=request.post_vars.address
    (latitude, longitude) = geocode(address)
    form.vars.lat = latitude
    form.vars.lng = longitude
    if form.process().accepted:
        redirect(URL('Events_Around_you'))
    return locals()

@auth.requires_login()
def going():
    db.user_event.insert(auth_user=session.auth.user.id, aevent=request.vars.id, status="Joined")
    response.flash = T('Successfully joined!')
    redirect(URL('Events_Around_you'))

    return locals()

@auth.requires_login()
def event():
    event = db(db.aevent.id == request.vars.id).select()
    stuff = event
    first = (db.user_event.auth_user == session.auth.user.id )
    second = (db.user_event.aevent == request.vars.id)
    joined = len(db( first & second ).select()) > 0
    count = len(db( second ).select())
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def Events_Around_you():
    stuff = db(db.aevent).select()
    things = crud.select(db.aevent)

    return locals()

def aevent():
    things = db( db.sponsor.id==db.aevent.sponsor).select(db.aevent.ALL, db.sponsor.host_reward, db.sponsor.part_reward, db.sponsor.name)
    return response.json(things)

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
