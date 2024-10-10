#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .name_15 import name as name_cls

class print_to_console(Command):
    """
    Print parameter value to console.
    
    Parameters
    ----------
        name : str
            Enter parameter name.
    
    """

    fluent_name = "print-to-console"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

