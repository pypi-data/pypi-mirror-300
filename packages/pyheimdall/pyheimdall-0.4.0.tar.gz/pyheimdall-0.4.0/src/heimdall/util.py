# -*- coding: utf-8 -*-

"""
Provides utilities functions around HERA elements tree refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

import heimdall
from lxml import etree


def _get_nodes(tree, tag, filter=None):
    nodes = tree.findall(f'.//{tag}')
    if filter:
        return [node for node in nodes if filter(node)]
    return nodes


def _get_node(tree, tag, filter=None):
    nodes = _get_nodes(tree, tag, filter)
    if len(nodes) == 0:
        return None
    if len(nodes) == 1:
        return nodes[0]
    raise IndexError(f"Too many {tag} elements ({len(nodes)})")


def _get_root(tree):
    return tree.xpath('//hera')[0]


def _create_nodes(parent, tag, text):
    nodes = list()
    if type(text) is str:
        node = _create_node(parent, tag, text)
        nodes.append(node)
    else:
        qname = etree.QName('http://www.w3.org/XML/1998/namespace', 'lang')
        for language_key, value in text.items():
            node = _create_node(parent, tag, value)
            node.set(qname, language_key)
            nodes.append(node)
    return nodes


def _create_node(parent, tag, text):
    node = etree.SubElement(parent, tag)
    node.text = text
    return node


def delete_unused_properties(tree, relational=True):
    """Delete unused properties from a HERA element tree.

    An unused property is not referenced by any attribute in the same tree
    (an attribute reuses a property via its ``pid``).
    Please note that if no attribute references a property, this property is
    deleted, even if one or more items in the tree reference this property.
    If an item metadata references an unused property,  the corresponding
    property is deleted anyway, as it has no use if the item's entity doesn't
    use the property via one of its attribute.

    | The previous paragraph description is valid for relational databases,
      but not for non-relational databases, where items directly use
      properties, and generally don't belong to any entities.
    | If your database is non-relational, a property isn't unused and
      shouldn't be deleted if one or more items reference it.
      To avoid this, set the ``relational`` parameter to ``False`` when using
      ``delete_unused_properties``.

    This function performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param relational: (optional, default: ``True``) Set this parameter
       to ``False`` for non-relational specific behaviour (see description)

    Usage ::

      >>> from heimdall.util import delete_unused_properties
      >>> ...  # create config, load HERA tree
      >>> delete_unused_properties(tree)  # get rid of some clutter

    """

    # give ourselves a map of unused properties, initialized with all of them
    properties = {}
    for p in heimdall.getProperties(tree):
        properties[p.get('id')] = p
    # let's check which properties are really unused
    for e in heimdall.getEntities(tree):
        for a in heimdall.getAttributes(e):
            pid = a.get('pid')
            if pid in properties.keys():
                # this property is in use ; so we mustn't delete it
                properties.pop(pid)

    to_keep = []
    if not relational:
        for pid in properties.keys():
            for item in heimdall.getItems(tree):
                metadata = heimdall.getMetadata(item, pid)
                if len(metadata) > 0:
                    # item references pid, so property won't be deleted
                    to_keep.append(pid)

    # the map now only contains unused ones ; so, delete them
    # (if not relational, pid in `to_keep` ARE NOT deleted)
    for pid, p in properties.items():
        if pid not in to_keep:
            p.getparent().remove(p)
    # end of function, don't bother with properties.clear()


def merge_properties(tree, properties):
    """Merge duplicate properties.

    This function allows to merge this similar properties into an existing one.
    This makes the resulting database schema more readable, because
    similarities between items and entities are more apparent when
    properties are systematically reused.

    This function updates ``pid`` referenced by each item's metadata,
    as long as the ``pid`` referenced by each entity's attribute, if
    these ``pid`` correspond to keys of the ``properties`` map parameter.
    The updated value is the key's value in ``properties``.

    Please note that only each relevant entity's attribute ``pid`` is
    modified, so each one keeps its custom names, descriptions and whatnot.

    | As each key of ``properties`` has its own value, this method
      can be used to merge many "duplicate" properties into different
      "factorized" ones, all at once.
    | However, each value of ``properties`` must be the unique
      identifier of an existing property in ``tree``.

    After using ``merge_properties``, previous duplicate properties
    remain in place, albeit now unused.
    Thus, ``heimdall.util.delete_unused_properties`` can be called
    on the same ``tree`` to get rid of them.

    This function performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param properties: Map containing old property identifiers as keys,
           and new property identifiers as values

    The example below shows how to reuse what is in fact the
    ``name`` property from Dublin Core, instead of entity-specific
    property names which are conceptually the same: ::

      >>> import heimdall
      >>> from heimdall.util import *
      >>> ...  # create config, load HERA tree
      >>> heimdall.createProperty(tree, 'dc:name', name="Name")
      >>> merge_properties(tree, {  # make reusage more apparent
      >>>     'book_title': 'dc:name',
      >>>     'author_name': 'dc:name',
      >>>     'character_name': 'dc:name',
      >>>     'thesaurus_keyword': 'dc:name',
      >>>     })
      >>> delete_unused_properties(tree)  # optional but nice
    """

    for item in heimdall.getItems(tree):
        for old, now in properties.items():
            metadata = heimdall.getMetadata(item, pid=old)
            for m in metadata:
                m.set('pid', now)

    for entity in heimdall.getEntities(tree):
        for old, now in properties.items():
            for attribute in heimdall.getAttributes(
                        entity, lambda a: a.get('pid') == old):
                heimdall.updateAttribute(attribute, pid=new)


class Relationship:
    def __init__(self, eid, source, target):
        self.eid = eid  # a Relationship is an Entity, it's its id
        self.source = source  # source attribute pid
        self.target = target  # target attribute pid


def refactor_relationship(tree, relationship, eid, euid, pid, cleanup=True):
    """TODO
    """
    # TODO only create property if not exists
    p = heimdall.createProperty(tree, pid=pid)
    e = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    # TODO only create attribute if not exists
    a = heimdall.createAttribute(e, pid=pid)
    # iterate over all items belonging to the relationship entity
    items = heimdall.getItems(tree, lambda n: n.get('eid') == relationship.eid)
    for old in items:
        source = heimdall.getMetadata(old, relationship.source)[0].text
        target = heimdall.getMetadata(old, relationship.target)[0].text

        def is_source(item):
            is_of_entity = item.get('eid') == eid
            has_unique_id = False
            # Unique id shouldn't be a repeatable attribute,
            # but we know what real world looks like. Thus,
            # try to not break in this edge case, and let's
            # hope our caller knows what she does.
            for v in heimdall.getValues(item, euid):
                has_unique_id = has_unique_id or (v == source)
            return is_of_entity and has_unique_id

        # get the item which must contain the new repeatable metadata
        now = heimdall.getItem(tree, is_source)
        etree.SubElement(now, 'metadata', pid=pid).text = target
        if cleanup:
            # delete `old` relationship item, because it is
            # now represented by new metadata in item `now`
            old.getparent().remove(old)
    if cleanup:
        # delete the `relationship` entity, as there are no more items using it
        heimdall.deleteEntity(tree, lambda n: n.get('id') == relationship.eid)


def merge_l10n_attributes(tree, entity, attr_vs_language, base_aid):
    """TODO
    """
    base = heimdall.getAttribute(entity, lambda a: a.get('id') == base_aid)
    amin = 0
    amax = 1
    for aid, language in attr_vs_language.items():
        attribute = heimdall.getAttribute(entity, lambda a: a.get('id') == aid)
        atype = _get_node(attribute, 'type')
        atype = atype.text if atype is not None else 'text'
        if atype != 'text':
            raise ValueError(f"Attribute '{aid}':'{type}' not localized")
        amin = max(amin, int(attribute.get('min')))
        amax = max(amax, int(attribute.get('max')))
        node = _get_node(attribute, 'name')
        qname = etree.QName('http://www.w3.org/XML/1998/namespace', 'lang')
        if node is not None:
            node.set(qname, language)
            base.append(node)
        node = _get_node(attribute, 'description')
        if node is not None:
            node.set(qname, language)
            base.append(node)

        pid = attribute.get('pid')
        for item in heimdall.getItems(tree):
            for metadata in heimdall.getMetadata(item):
                if metadata.get('pid') == pid:
                    metadata.set('pid', base.get('pid'))
                    metadata.set(qname, language)

        if aid == base_aid:
            continue
        attribute.getparent().remove(attribute)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
