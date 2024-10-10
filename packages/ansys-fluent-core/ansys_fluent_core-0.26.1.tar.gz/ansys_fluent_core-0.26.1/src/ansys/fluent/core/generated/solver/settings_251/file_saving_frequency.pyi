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

from .volume_heat_run import volume_heat_run as volume_heat_run_cls
from .face_heat_run import face_heat_run as face_heat_run_cls
from .face_temperature_run import face_temperature_run as face_temperature_run_cls
from .joule_heat_run import joule_heat_run as joule_heat_run_cls

class file_saving_frequency(Group):
    fluent_name = ...
    child_names = ...
    volume_heat_run: volume_heat_run_cls = ...
    face_heat_run: face_heat_run_cls = ...
    face_temperature_run: face_temperature_run_cls = ...
    joule_heat_run: joule_heat_run_cls = ...
