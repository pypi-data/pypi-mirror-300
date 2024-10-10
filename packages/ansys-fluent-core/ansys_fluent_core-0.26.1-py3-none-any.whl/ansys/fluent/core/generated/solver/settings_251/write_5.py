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

from .object_name_3 import object_name as object_name_cls
from .file_name_14 import file_name as file_name_cls

class write(Command):
    """
    Write the Cumulative Forces/Moments.
    
    Parameters
    ----------
        object_name : str
            Select cumulative-plot object.
        file_name : str
            Enter the name you want the file saved with.
    
    """

    fluent_name = "write"

    argument_names = \
        ['object_name', 'file_name']

    _child_classes = dict(
        object_name=object_name_cls,
        file_name=file_name_cls,
    )

