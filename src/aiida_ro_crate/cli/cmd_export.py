# -*- coding: utf-8 -*-
"""CLI command to export part of an AiiDA provenance graph to a RO-crate."""
from aiida.cmdline.params import options
import click

from .cli import cmd_root


@cmd_root.command('export')
@options.NODES()
def cmd_export(nodes):
    """Export part of an AiiDA provenance graph to an RO-crate."""
    from aiida.manage import get_manager
    from aiida.orm import Computer, Group, Node, QueryBuilder, User, entities
    from aiida.tools.archive.create import _collect_required_entities

    storage_backend = get_manager().get_profile_storage()
    traversal_rules = {
        'input_calc_forward': False,
        'input_work_forward': True,
        'create_backward': True,
        'return_backward': True,
        'call_calc_backward': True,
        'call_work_backward': True,
    }

    entity_ids: Dict[entities.EntityTypes, Set[int]] = {
        entity: set() for entity in [
            entities.EntityTypes.USER,
            entities.EntityTypes.COMPUTER,
            entities.EntityTypes.AUTHINFO,
            entities.EntityTypes.GROUP,
            entities.EntityTypes.NODE,
            entities.EntityTypes.COMMENT,
            entities.EntityTypes.LOG,
        ]
    }

    for entry in nodes:
        if isinstance(entry, Group):
            entity_ids[entities.EntityTypes.GROUP].add(entry.pk)
        elif isinstance(entry, Node):
            entity_ids[entities.EntityTypes.NODE].add(entry.pk)
        elif isinstance(entry, Computer):
            entity_ids[entities.EntityTypes.COMPUTER].add(entry.pk)
        elif isinstance(entry, User):
            entity_ids[entities.EntityTypes.USER].add(entry.pk)

    query = QueryBuilder
    group_nodes, link_data = _collect_required_entities(
        query, entity_ids, traversal_rules, False, False, False, storage_backend, 100
    )

    print(group_nodes, link_data)
