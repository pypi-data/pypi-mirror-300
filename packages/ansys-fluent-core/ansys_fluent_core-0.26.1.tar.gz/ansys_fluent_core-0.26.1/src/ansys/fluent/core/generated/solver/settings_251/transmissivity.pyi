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

from .v_transmissivity import v_transmissivity as v_transmissivity_cls
from .ir_transmissivity import ir_transmissivity as ir_transmissivity_cls
from .d_transmissivity import d_transmissivity as d_transmissivity_cls

class transmissivity(Group):
    fluent_name = ...
    child_names = ...
    v_transmissivity: v_transmissivity_cls = ...
    ir_transmissivity: ir_transmissivity_cls = ...
    d_transmissivity: d_transmissivity_cls = ...
