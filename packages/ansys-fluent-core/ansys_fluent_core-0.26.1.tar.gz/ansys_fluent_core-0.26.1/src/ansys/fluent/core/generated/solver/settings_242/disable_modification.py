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

from .mod_name import mod_name as mod_name_cls

class disable_modification(Command):
    """
    Disable a single defined case modification.
    
    Parameters
    ----------
        mod_name : str
            'mod_name' child.
    
    """

    fluent_name = "disable-modification"

    argument_names = \
        ['mod_name']

    _child_classes = dict(
        mod_name=mod_name_cls,
    )

