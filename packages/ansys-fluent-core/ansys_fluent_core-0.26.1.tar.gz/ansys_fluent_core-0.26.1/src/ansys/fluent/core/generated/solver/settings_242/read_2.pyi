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

from .filename_1 import filename as filename_cls
from .unit_1 import unit as unit_cls

class read(Command):
    fluent_name = ...
    argument_names = ...
    filename: filename_cls = ...
    unit: unit_cls = ...
