#!/usr/bin/env python
"""Contains the Unit Tests for the REST Resources.

Contains the Unit Tests for exercising all provided
API Endpoints for the Python Eve REST Server
"""

import requests

__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"


ROOT_TEST_URL = 'http://localhost:5005'


def test_default_no_content_type_response():
    """ Read Base URL without Content Type"""
    url = ROOT_TEST_URL
    headers = {}
    r = requests.get(url, headers=headers)
    assert r.status_code == requests.codes.ok  # 200
