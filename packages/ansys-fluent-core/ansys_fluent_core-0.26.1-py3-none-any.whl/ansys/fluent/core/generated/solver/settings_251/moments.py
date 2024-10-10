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

from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_of_moments import num_of_moments as num_of_moments_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .filename_1_4 import filename_1 as filename_1_cls

class moments(Command):
    """
    Set moments for population balance.
    
    Parameters
    ----------
        surface_list : List
            Select surface.
        volume_list : List
            Enter cell zone name list.
        num_of_moments : int
            'num_of_moments' child.
        write_to_file : bool
            'write_to_file' child.
        filename_1 : str
            'filename' child.
    
    """

    fluent_name = "moments"

    argument_names = \
        ['surface_list', 'volume_list', 'num_of_moments', 'write_to_file',
         'filename']

    _child_classes = dict(
        surface_list=surface_list_cls,
        volume_list=volume_list_cls,
        num_of_moments=num_of_moments_cls,
        write_to_file=write_to_file_cls,
        filename=filename_1_cls,
    )

