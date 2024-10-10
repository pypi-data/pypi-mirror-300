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

from .name_7 import name as name_cls

class list_properties(Command):
    """
    List case material properties.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

