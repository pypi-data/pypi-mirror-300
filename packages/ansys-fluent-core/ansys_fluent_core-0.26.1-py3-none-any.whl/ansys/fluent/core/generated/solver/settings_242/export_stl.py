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

from .file_name_25 import file_name as file_name_cls

class export_stl(Command):
    """
    Export specified surfaces from as an .stl file.
    
    Parameters
    ----------
        file_name : str
            Export specified surfaces from 3D cases as an .stl file.
    
    """

    fluent_name = "export-stl"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

