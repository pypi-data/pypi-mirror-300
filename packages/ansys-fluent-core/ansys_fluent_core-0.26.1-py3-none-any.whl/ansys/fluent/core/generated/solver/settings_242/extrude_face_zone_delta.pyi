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

from .face_zone import face_zone as face_zone_cls
from .distance_delta import distance_delta as distance_delta_cls

class extrude_face_zone_delta(Command):
    fluent_name = ...
    argument_names = ...
    face_zone: face_zone_cls = ...
    distance_delta: distance_delta_cls = ...
