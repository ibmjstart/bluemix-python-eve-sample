#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides Event Hooks against REST Resources.

This module is the mastermind controlling the
flow of triggers and events to resources
"""

import traceback
from settings import (LANGUAGES)

__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"


def before_returning_irrational_items(request, lookup):
    try:
        desiredLang = request.accept_languages.best_match(LANGUAGES.keys())
        print "The Accept-Language Header is: " + desiredLang
        lookup["locale"] = {"$eq": desiredLang or "en"}
    except Exception, e:
        print e
        traceback.print_exc()
