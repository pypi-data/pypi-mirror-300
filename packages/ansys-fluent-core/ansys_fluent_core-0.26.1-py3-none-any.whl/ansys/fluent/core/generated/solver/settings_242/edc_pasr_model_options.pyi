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

from .edc_pasr_mixing_model import edc_pasr_mixing_model as edc_pasr_mixing_model_cls
from .mixing_constant import mixing_constant as mixing_constant_cls
from .fractal_dimension import fractal_dimension as fractal_dimension_cls

class edc_pasr_model_options(Group):
    fluent_name = ...
    child_names = ...
    edc_pasr_mixing_model: edc_pasr_mixing_model_cls = ...
    mixing_constant: mixing_constant_cls = ...
    fractal_dimension: fractal_dimension_cls = ...
