#Name: Sandeep Raveendran Thandassery
#Course Number: CSE 6331 Section 004
#Lab Number: 7
'''Copyright (c) 2015 HG,DL,UTA
   Authentication component'''

# -*- coding: utf-8 -*-

from functools import wraps
from flask import request, Response, session
import database as app_data
import hashlib


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    print('username - {}, pwd - {}'.format(username, password))
    status = False
    if 'user_id' in session:
        status = True
    else:
        print 'here'
        hash_pwd = hashlib.sha256(password).hexdigest()
        print 'here'
        app_data.autheticate_user(username, hash_pwd)
        session['user_id']=username
        status = True
    return status

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
