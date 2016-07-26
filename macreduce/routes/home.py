#!/usr/bin/env python
"""Provides custom routes against REST Resources.

This module overrides the home/index default route
for the Python Eve server.  It provides a simple
html page as well as supporting requests accepting
application/json .
"""

import os
import traceback
from settings import (APP_URI)
from flask import send_from_directory, Response, request, json
from settings import REDIS_INSTANCE, VCAP_CONFIG
from functools import wraps
from helpers import oui
from gevent import Timeout
from datetime import datetime, timedelta

# capture current working directory
PWD = os.environ.get("PWD")
# set static folder path for static data
static_folder = os.path.join(PWD, "macreduce/static")
vcap = os.environ.get("VCAP_SERVICES")


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'bluemix' and password == 'devfun'


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


def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json',
                     'application/json; charset=utf-8',
                     'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


def run_once_per_day(f):
    def wrapper(*args, **kwargs):
        try:
            # Phase 1:  Calculate refresh and current date to determine
            #           if whether to download a new copy of the MAC
            #           txt file should be downloaded from the IEEE site.
            #           We do not want to repopulate more than once a day
            # Are we running on Bluemix or not?
            if VCAP_CONFIG:
                nextDate = REDIS_INSTANCE.get("nextDate")
                # Nothing stored for first time this app has been deployed
                if nextDate is None:
                    nextDate = datetime.utcnow()
                else:
                    # Need to convert the cached date from str to datetime
                    nextDate = datetime.strptime(nextDate,
                                                 '%Y-%m-%d %H:%M:%S.%f')
            else:
                # Running local.  First time?
                if not wrapper.has_run:
                    nextDate = datetime.utcnow()
                # We've already populated so let's not populate again
                else:
                    nextDate = datetime.utcnow() + timedelta(seconds=86400)
            # Let's record what datetime it is right now ...
            now = datetime.utcnow()

            # Phase 2:  Test whether the current date is past our 24 hour
            #           refresh date criteria or not.
            print("Evaluating if Now is >= Criteria ...")
            if now >= nextDate:
                print("Refresh criteria has been met")
                # Set a flag so that future local repopulates fall through
                wrapper.has_run = True
                # Test if we are running in Bluemix
                if VCAP_CONFIG:
                    # Persist a refresh date 24 hours in the future
                    REDIS_INSTANCE.set("nextDate", datetime.utcnow()
                                       + timedelta(seconds=86400))
                return f(*args, **kwargs)
            else:
                # Refresh not required, relay a default response
                print("Refresh criteria NOT met")
                data = {
                    'message': 'Whoaa! MacReduce Data is up to date!'
                }
                message = json.dumps(data)
                print(message)
                resp = Response(message,
                                status=200,
                                mimetype='application/json')
                return resp
        except Exception as e:
            print(e)
            print(traceback.format_exc())
    wrapper.has_run = False
    return wrapper


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def index(path=''):
    if request_wants_json():
        data = {
            'message': 'Welcome to the macReduce API Backend Sample '
            'powered by IBM Bluemix.'
        }
        message = json.dumps(data)
        resp = Response(message, status=200, mimetype='application/json')
        resp.headers['Link'] = APP_URI
        return resp
    else:
        return send_from_directory(static_folder, "index.html")


# Let's protect this custom endpoint with basic auth and frequency control
@requires_auth
@run_once_per_day
def populate():
    print("Begin MAC Address population ...")
    try:
        with Timeout(300):
            oui.update()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    # Response needed for local execution which runs shorter than 2 mins
    finally:
        data = {
            'message': 'Whoaa! MacReduce Data Populated/Refreshed'
        }
        message = json.dumps(data)
        print(message)
        resp = Response(message, status=200, mimetype='application/json')
        return resp


def favicon():
    return send_from_directory(os.path.join(static_folder, "img"),
                               "favicon.ico")
