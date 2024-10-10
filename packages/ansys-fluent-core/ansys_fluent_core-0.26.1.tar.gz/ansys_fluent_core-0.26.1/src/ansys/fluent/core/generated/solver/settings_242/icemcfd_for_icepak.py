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

from .file_name_1 import file_name as file_name_cls

class icemcfd_for_icepak(Command):
    """
    Write a binary ICEMCFD domain file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
    
    """

    fluent_name = "icemcfd-for-icepak"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

