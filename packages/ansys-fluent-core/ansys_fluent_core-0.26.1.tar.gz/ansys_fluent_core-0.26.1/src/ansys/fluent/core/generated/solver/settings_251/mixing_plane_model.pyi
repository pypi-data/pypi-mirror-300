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

from typing import Union, List, Tuple

from .bands_type import bands_type as bands_type_cls
from .number_of_bands import number_of_bands as number_of_bands_cls
from .list_mixing_planes import list_mixing_planes as list_mixing_planes_cls

class mixing_plane_model(Group):
    fluent_name = ...
    child_names = ...
    bands_type: bands_type_cls = ...
    number_of_bands: number_of_bands_cls = ...
    command_names = ...

    def list_mixing_planes(self, ):
        """
        Display the configuration settings of mixing planes in the current case.
        """

