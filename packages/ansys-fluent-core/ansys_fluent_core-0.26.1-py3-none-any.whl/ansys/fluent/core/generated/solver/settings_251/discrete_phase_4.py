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

from .bc_type_2 import bc_type as bc_type_cls
from .reinject_using_injection import reinject_using_injection as reinject_using_injection_cls
from .bc_user_function import bc_user_function as bc_user_function_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls

class discrete_phase(Group):
    """
    Allows to change DPM model variables or settings.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['bc_type', 'reinject_using_injection', 'bc_user_function',
         'dem_collision_partner']

    _child_classes = dict(
        bc_type=bc_type_cls,
        reinject_using_injection=reinject_using_injection_cls,
        bc_user_function=bc_user_function_cls,
        dem_collision_partner=dem_collision_partner_cls,
    )

    _child_aliases = dict(
        discrete_phase_bc_function="bc_user_function",
        discrete_phase_bc_type="bc_type",
        dpm_bc_collision_partner="dem_collision_partner",
        dpm_bc_type="bc_type",
        dpm_bc_udf="bc_user_function",
        reinj_inj="reinject_using_injection",
    )

