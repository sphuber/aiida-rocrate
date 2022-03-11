# -*- coding: utf-8 -*-
"""Command line interface for ``aiida-ro-crate``."""
from aiida.cmdline.params import options, types
import click


@click.group()
@options.PROFILE(type=types.ProfileParamType(load_profile=True), expose_value=False)
@options.VERBOSITY()
def cmd_root():
    """Command line interface for Research Object Crate interoperability with AiiDA."""
