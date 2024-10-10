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

from .host_file import host_file as host_file_cls

class save_hosts(Command):
    """
    Write a hosts file.
    
    Parameters
    ----------
        host_file : str
            'host_file' child.
    
    """

    fluent_name = "save-hosts"

    argument_names = \
        ['host_file']

    _child_classes = dict(
        host_file=host_file_cls,
    )

    return_type = "<object object at 0x7fd93f6c4d90>"
