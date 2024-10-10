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

from .vof_from_min_limit import vof_from_min_limit as vof_from_min_limit_cls
from .vof_from_max_limit import vof_from_max_limit as vof_from_max_limit_cls
from .vof_to_min_limit import vof_to_min_limit as vof_to_min_limit_cls
from .vof_to_max_limit import vof_to_max_limit as vof_to_max_limit_cls
from .ia_norm_min_limit import ia_norm_min_limit as ia_norm_min_limit_cls
from .max_rel_humidity import max_rel_humidity as max_rel_humidity_cls

class evaporation_condensation(Group):
    """
    Evaporation-condensation advanced options menu.
    """

    fluent_name = "evaporation-condensation"

    child_names = \
        ['vof_from_min_limit', 'vof_from_max_limit', 'vof_to_min_limit',
         'vof_to_max_limit', 'ia_norm_min_limit', 'max_rel_humidity']

    _child_classes = dict(
        vof_from_min_limit=vof_from_min_limit_cls,
        vof_from_max_limit=vof_from_max_limit_cls,
        vof_to_min_limit=vof_to_min_limit_cls,
        vof_to_max_limit=vof_to_max_limit_cls,
        ia_norm_min_limit=ia_norm_min_limit_cls,
        max_rel_humidity=max_rel_humidity_cls,
    )

