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

from .skewness_correction_itr import skewness_correction_itr as skewness_correction_itr_cls
from .neighbor_correction_itr import neighbor_correction_itr as neighbor_correction_itr_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .vof_correction_itr import vof_correction_itr as vof_correction_itr_cls
from .explicit_momentum_under_relaxation import explicit_momentum_under_relaxation as explicit_momentum_under_relaxation_cls
from .explicit_pressure_under_relaxation import explicit_pressure_under_relaxation as explicit_pressure_under_relaxation_cls
from .flow_courant_number import flow_courant_number as flow_courant_number_cls
from .volume_fraction_courant_number import volume_fraction_courant_number as volume_fraction_courant_number_cls
from .explicit_volume_fraction_under_relaxation import explicit_volume_fraction_under_relaxation as explicit_volume_fraction_under_relaxation_cls

class p_v_controls(Group):
    fluent_name = ...
    child_names = ...
    skewness_correction_itr: skewness_correction_itr_cls = ...
    neighbor_correction_itr: neighbor_correction_itr_cls = ...
    skewness_neighbor_coupling: skewness_neighbor_coupling_cls = ...
    vof_correction_itr: vof_correction_itr_cls = ...
    explicit_momentum_under_relaxation: explicit_momentum_under_relaxation_cls = ...
    explicit_pressure_under_relaxation: explicit_pressure_under_relaxation_cls = ...
    flow_courant_number: flow_courant_number_cls = ...
    volume_fraction_courant_number: volume_fraction_courant_number_cls = ...
    explicit_volume_fraction_under_relaxation: explicit_volume_fraction_under_relaxation_cls = ...
    return_type = ...
