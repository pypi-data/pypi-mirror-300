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

from .zone_names_4 import zone_names as zone_names_cls

class create_multiple_zone_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    zone_names: zone_names_cls = ...
    return_type = ...
