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

from .skewness_correction_itr_count import skewness_correction_itr_count as skewness_correction_itr_count_cls
from .neighbor_correction_itr_count import neighbor_correction_itr_count as neighbor_correction_itr_count_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .vof_correction_itr_count import vof_correction_itr_count as vof_correction_itr_count_cls
from .flow_courant_number import flow_courant_number as flow_courant_number_cls
from .volume_fraction_courant_number import volume_fraction_courant_number as volume_fraction_courant_number_cls
from .explicit_pressure_under_relaxation import explicit_pressure_under_relaxation as explicit_pressure_under_relaxation_cls
from .explicit_momentum_under_relaxation import explicit_momentum_under_relaxation as explicit_momentum_under_relaxation_cls
from .explicit_volume_fraction_under_relaxation import explicit_volume_fraction_under_relaxation as explicit_volume_fraction_under_relaxation_cls

class p_v_controls(Group):
    """
    Set P-V-Controls.
    """

    fluent_name = "p-v-controls"

    child_names = \
        ['skewness_correction_itr_count', 'neighbor_correction_itr_count',
         'skewness_neighbor_coupling', 'vof_correction_itr_count',
         'flow_courant_number', 'volume_fraction_courant_number',
         'explicit_pressure_under_relaxation',
         'explicit_momentum_under_relaxation',
         'explicit_volume_fraction_under_relaxation']

    _child_classes = dict(
        skewness_correction_itr_count=skewness_correction_itr_count_cls,
        neighbor_correction_itr_count=neighbor_correction_itr_count_cls,
        skewness_neighbor_coupling=skewness_neighbor_coupling_cls,
        vof_correction_itr_count=vof_correction_itr_count_cls,
        flow_courant_number=flow_courant_number_cls,
        volume_fraction_courant_number=volume_fraction_courant_number_cls,
        explicit_pressure_under_relaxation=explicit_pressure_under_relaxation_cls,
        explicit_momentum_under_relaxation=explicit_momentum_under_relaxation_cls,
        explicit_volume_fraction_under_relaxation=explicit_volume_fraction_under_relaxation_cls,
    )

    _child_aliases = dict(
        neighbor_correction_itr_count="solution/methods/p_v_coupling/neighbor_correction_itr_count",
        skewness_correction_itr_count="solution/methods/p_v_coupling/skewness_correction_itr_count",
        skewness_neighbor_coupling="solution/methods/p_v_coupling/skewness_neighbor_coupling",
    )

