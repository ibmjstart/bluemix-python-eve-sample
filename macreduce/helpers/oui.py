#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Instantiates a helper class to interact with the oui
MA-L resource.

This is a helper class
"""

import re
import requests
import urllib2
from settings import VCAP_CONFIG
from gevent import Timeout
from eve.methods.post import post_internal
from eve.methods.delete import delete

__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"

OUI_URL = "http://standards-oui.ieee.org/oui.txt"
OUI_HEX_REGEX = "[A-Za-z0-9]{2}-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}"
OUI_MATCH = "-"
OUI_REPLACE = ":"


def update():
    print "Deleting (reset) Mongo Collection named 'mac'"
    delete("mac")
    with Timeout(5, False):
        oui = urllib2.urlopen(OUI_URL, timeout=240)
    # code, oui = _sendGetRequest(OUI_URL, {}, {})
    # print "IEEE Response Code was a " + str(code)
    count = 1
    for totalcount, line in enumerate(oui, start=1):
        macHexVendor = re.match("^.*(" + OUI_HEX_REGEX + ").*"
                                + "hex" + ".*?([A-Z].*)$", line)
        if macHexVendor:
            count += 1
            macEntry = {
                "base16": macHexVendor.group(1).replace(OUI_MATCH,
                                                        ""),
                "hex": macHexVendor.group(1).replace(OUI_MATCH,
                                                     OUI_REPLACE),
                "organization": macHexVendor.group(2)
            }
            post_internal("mac", macEntry)
            if not VCAP_CONFIG:
                print macHexVendor.group(1).replace(OUI_MATCH,
                                                    OUI_REPLACE) + ", " + \
                    macHexVendor.group(2)
    print "Number of MAC Entries matched: " + str(count)
    return ""


# requests status codes:
# https://github.com/kennethreitz/requests/blob/master/requests/status_codes.py
def _sendGetRequest(url, queryParameters, customHeaders):
    commonHeaders = {"User-Agent": "macReduce"}
    headers = dict(commonHeaders.items() + customHeaders.items())
    req = requests.Request('GET', url, params=queryParameters,
                           headers=headers)
    prepared = req.prepare()
    s = requests.Session()
    print "Retrieving data from url: " + url
    r = s.send(prepared)
    return r.status_code, r.text
