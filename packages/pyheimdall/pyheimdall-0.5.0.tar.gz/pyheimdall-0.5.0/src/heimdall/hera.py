# -*- coding: utf-8 -*-
from lxml import etree
from urllib.parse import urlparse
from urllib.request import urlopen


def getDatabase(db):
    if not is_url(db.url):
        tree = etree.parse(db.url)
        # can raise OSError (file not found, ...)
    else:
        with urlopen(db.url) as response:
            tree = etree.fromstring(response.read().decode())
            # can raise urllib.error.HTTPError (HTTP Error 404: Not Found, ...)
    return tree


def is_url(path):
    schemes = ('http', 'https', )
    return urlparse(path).scheme in schemes
