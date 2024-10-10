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

from .filename_6 import filename as filename_cls

class read_from_file(Command):
    """
    Read data from file.
    
    Parameters
    ----------
        filename : str
            Enter file name.
    
    """

    fluent_name = "read-from-file"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

