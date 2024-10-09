# -*- coding: utf-8 -*-
from json import load, loads
from urllib.parse import urlparse
from urllib.request import urlopen
from lxml import etree


def getDatabase(db):
    if not is_url(db.url):
        with open(db.url, 'r') as f:
            data = load(f)
    else:
        with urlopen(db.url) as response:
            data = loads(response.read().decode())
    return _create_tree(data)


def is_url(path):
    schemes = ('http', 'https', )
    return urlparse(path).scheme in schemes


def _create_tree(data):
    url_xmlschema = "http://www.w3.org/2001/XMLSchema-instance"
    url_hera = "https://gitlab.huma-num.fr/datasphere/hera/schema/schema.xsd"
    qname = etree.QName(url_xmlschema, "schemaLocation")
    root = etree.Element('hera', {qname: url_hera})

    # create Properties if any
    properties = data.get('properties', None)
    if properties is not None:
        elements = etree.SubElement(root, 'properties')
        for o in properties:
            uid = o['@id']  # @id is mandatory
            e = etree.SubElement(elements, 'property', id=uid)
            _add_xml_element_from_json(e, o, 'type')
            _add_xml_element_from_json(e, o, 'name')
            _add_xml_element_from_json(e, o, 'description')
            # _add_xml_element_from_json(e, o, 'uris')  # TODO property.uris

    # create Entities if any
    entities = data.get('entities', None)
    if entities is not None:
        elements = etree.SubElement(root, 'entities')
        # TODO entities

    # create Items if any
    items = data.get('items', None)
    if items is not None:
        elements = etree.SubElement(root, 'items')
        for o in items:
            e = etree.SubElement(elements, 'item')
            _add_attribute_from_json(e, o, 'eid')
            metadata = o.get('metadata', [])
            for m in metadata:
                pid = m['pid']  # pid is mandatory
                meta = etree.SubElement(e, 'metadata', pid=pid)
                meta.text = m['value']  # value is mandatory, too

    return etree.ElementTree(root)


def _add_xml_element_from_json(e, o, attr):
    value = o.get(attr, None)
    if value is not None:
        sub = etree.SubElement(e, attr)
        sub.text = value


def _add_attribute_from_json(e, o, attr):
    value = o.get(attr, None)
    if value is not None:
        e.set(attr, value)
