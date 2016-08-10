#!/usr/bin/env python
"""Contains the Unit Tests for the REST Resources.

Contains the Unit Tests for exercising all provided
API Endpoints for the Python Eve REST Server.
HTTP Header Reference:
https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
"""

import requests
from xml.etree import ElementTree  # Import an XML parser

__author__ = "Sanjay Joshi"
__copyright__ = "Copyright 2016 IBM"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Demo"


ROOT_TEST_URL = 'http://localhost:5005'
API_PATH = '/api/v1'


def test_default_no_content_type_response():
    """ Read base API RESOURCES URL WITHOUT Accept request header"""
    expectedJSON = {"_links": {"child": [{"href": "mac", "title": "mac"}]}}
    url = ''.join([ROOT_TEST_URL, API_PATH])
    headers = {}
    r = requests.get(url, headers=headers)
    assert r.status_code == requests.codes.ok  # 200
    assert r.json() == expectedJSON  # Match Expected


def test_accept_content_type_app_json_response():
    """ Read base API RESOURCES URL WITH JSON Accept request header"""
    expectedJSON = {"_links": {"child": [{"href": "mac", "title": "mac"}]}}
    url = ''.join([ROOT_TEST_URL, API_PATH])
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    assert r.status_code == requests.codes.ok  # 200
    assert r.json() == expectedJSON  # Match Expected


def test_accept_content_type_app_xml_response():
    """ Read base API RESOURCES URL WITH XML Accept request header"""
    expectedXML = ('<resource><link rel="child" '
                   'href="mac" title="mac" /></resource>')
    url = ''.join([ROOT_TEST_URL, API_PATH])
    headers = {'Accept': 'application/xml'}
    r = requests.get(url, headers=headers)
    objResponse = ElementTree.fromstring(r.content)
    link = objResponse.findall('link')
    assert r.status_code == requests.codes.ok  # 200
    assert objResponse.tag == 'resource'  # Root Node
    assert len(link) == 1  # One Link Child
    assert r.content == expectedXML  # Match Expected
