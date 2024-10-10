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

from .fixed_cycle_parameters import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters import coarsening_parameters as coarsening_parameters_cls
from .global_dt_smoother_type import global_dt_smoother_type as global_dt_smoother_type_cls
from .smoother_type import smoother_type as smoother_type_cls

class amg_controls_scalar(Group):
    """
    Enter AMG scalar parameters menu.
    """

    fluent_name = "amg-controls-scalar"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters',
         'global_dt_smoother_type', 'smoother_type']

    _child_classes = dict(
        fixed_cycle_parameters=fixed_cycle_parameters_cls,
        coarsening_parameters=coarsening_parameters_cls,
        global_dt_smoother_type=global_dt_smoother_type_cls,
        smoother_type=smoother_type_cls,
    )

