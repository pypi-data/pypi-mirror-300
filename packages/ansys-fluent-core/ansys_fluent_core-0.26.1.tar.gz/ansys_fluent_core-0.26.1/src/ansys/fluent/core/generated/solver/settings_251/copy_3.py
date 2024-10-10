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

from .command_name import command_name as command_name_cls

class copy(Command):
    """
    Copy an execute-command.
    
    Parameters
    ----------
        command_name : str
            'command_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['command_name']

    _child_classes = dict(
        command_name=command_name_cls,
    )

