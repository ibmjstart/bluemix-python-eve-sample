#!/usr/bin/env python
"""Contains the Data Model for the MAC Address(es) Resource.

Represents the data model for the IEEE MA-L Public Assignments
Listing data.  The three-octet MA-L can be used as a lookup
to help identify a provided Organizationally Unique Identifier
(OUI) which identifies a vendor, manufacturer or other org
globally/worldwide.
ref: http://standards.ieee.org/develop/regauth/oui/public.html
"""
__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"

schema = {
    'schema': {
        'cloudhost': {
            'type': 'string',
            'default': 'Powered by IBM Bluemix and Python Eve'
        },
        'base16': {
            'type': 'string',
            'default': '######'
        },
        'hex': {
            'type': 'string',
            'default': '##-##-##'
        },
        'organization': {
            'type': 'string',
            'default': 'Doh!MissingOrg'
        }
    },
    'allow_unknown': True
}
