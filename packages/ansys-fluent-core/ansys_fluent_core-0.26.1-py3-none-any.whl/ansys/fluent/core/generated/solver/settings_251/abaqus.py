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
from .surface_name_list import surface_name_list as surface_name_list_cls
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls

class abaqus(Command):
    """
    Write an ABAQUS file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        surface_name_list : List
            List of surfaces to export.
        structural_analysis : bool
            Choose whether structural analysis or not.
        write_loads : bool
            Choose whether or not to write loads.
        loads : List
            Choose the structural loads type to export.
    
    """

    fluent_name = "abaqus"

    argument_names = \
        ['file_name', 'surface_name_list', 'structural_analysis',
         'write_loads', 'loads']

    _child_classes = dict(
        file_name=file_name_cls,
        surface_name_list=surface_name_list_cls,
        structural_analysis=structural_analysis_cls,
        write_loads=write_loads_cls,
        loads=loads_cls,
    )

