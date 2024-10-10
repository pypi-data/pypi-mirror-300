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

from .file_name_24 import file_name as file_name_cls

class optimal_displacements(Command):
    """
    Export the computed optimal displacements.
    
    Parameters
    ----------
        file_name : str
            Displacements file name.
    
    """

    fluent_name = "optimal-displacements"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

