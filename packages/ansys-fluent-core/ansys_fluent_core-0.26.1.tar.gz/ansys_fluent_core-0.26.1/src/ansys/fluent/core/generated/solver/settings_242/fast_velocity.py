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

class fast_velocity(Command):
    """
    Write a FAST/Plot3D unstructured vector function file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
    
    """

    fluent_name = "fast-velocity"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

