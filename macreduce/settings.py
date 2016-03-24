#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Instantiates the Python Eve REST API Server.

Instantiates the Python Eve REST API Server for both local
and cloud (IBM Bluemix) execution.  Provides a default catch-all
routing to provide API consumers with intentional responses
for all routes.  Provides a redis cloud caching instance for
session management where desired.
"""

import os
import json
import re
import redis
from models import (mac)

__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"

# Initialize Objects
# capture current working directory
PWD = os.getenv("PWD")
# set root folder path
ROOT_PATH = os.path.join(PWD, "macreduce")
# set default host and ports (change 5000 to avoid airplay collision)
APP_HOST = os.getenv('VCAP_APP_HOST', '0.0.0.0')
APP_PORT = os.getenv('VCAP_APP_PORT', '5005')
VCAP_CONFIG = os.getenv('VCAP_SERVICES')
VCAP_APPLICATION = os.getenv('VCAP_APPLICATION')
REDIS_INSTANCE = None
APP_URI = 'http://0.0.0.0:5005'

# Detect if we are deployed within Bluemix or not and act accordingly
if VCAP_CONFIG:
    # We're hosted on Bluemix! Use the MongoLabs sandbox as our backend.
    # Read the VCAP_APPLICATION environment variable to get its route
    decoded_application = json.loads(VCAP_APPLICATION)
    APP_URI = 'http://' + decoded_application['application_uris'][0]
    SERVER_NAME = decoded_application['application_uris'][0]
    # Read the VCAP_SERVICES environment variable
    decoded_config = json.loads(VCAP_CONFIG)
    # Loop through the service instances to capture connection info
    for key, value in decoded_config.iteritems():
        # Looking for an instance of a Mongo Bluemix Service
        if key.startswith('mongo'):
            mongo_creds = decoded_config[key][0]['credentials']
            seq = (r'^mongodb\:\/\/(?P<username>[\W\w]+):(?P<password>[\W\w]+)@'
                   '(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[\W\w]+).*?$')
            regex = re.compile(seq)
            match = regex.search(mongo_creds['url'])
            # Deconstruct MongoURL connection information
            parseURI = match.groupdict()
            MONGO_HOST = parseURI['host']
            MONGO_PORT = int(parseURI['port'])
            MONGO_USERNAME = parseURI['username']
            MONGO_PASSWORD = parseURI['password']
            MONGO_DBNAME = parseURI['database']
            continue
        # Looking for an instance of Redis
        elif key.startswith('redis'):
            redis_creds = decoded_config[key][0]['credentials']
            REDIS_HOSTNAME = redis_creds['hostname']
            REDIS_PASSWORD = redis_creds['password']
            REDIS_PORT = int(redis_creds['port'])
            REDIS_INSTANCE = (redis.Redis(host=REDIS_HOSTNAME,
                              password=REDIS_PASSWORD, port=REDIS_PORT))
            continue

else:
    # We're on my favorite Mac Laptop
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'apitest'

# Enable URL_PREFIX.  Used in conjunction with API_VERSION to build
# API Endpoints of the form <base_route>/<url_prefix>/<api_version>/
URL_PREFIX = 'api'

# Enable API Versioning.  This will force API Calls to follow a form of
# <base_route>/<api_version>/<resource_title>/...
API_VERSION = 'v1'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

MONGO_QUERY_BLACKLIST = ['$where']
# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose the following resources (MongoDB collections):
# 'mac', ...
# In order to allow for proper data validation, we define behaviour
# and structure.
DOMAIN = {
    'mac': mac.schema,
}
