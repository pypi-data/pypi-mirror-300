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

from .option_9 import option as option_cls
from .max_vf_allowed_for_blocking import max_vf_allowed_for_blocking as max_vf_allowed_for_blocking_cls
from .drag_scaling_enabled import drag_scaling_enabled as drag_scaling_enabled_cls
from .source_term_scaling_enabled import source_term_scaling_enabled as source_term_scaling_enabled_cls

class volume_displacement(Group):
    """
    In many Lagrangian-Eulerian simulations, the volume fraction of the local particle phase may not be small,
    and the blocking effect of the particulate phase on the carrier phase may need to be taken into account.
    To enable the volume displacement effect of particles, select "option = #t".
    """

    fluent_name = "volume-displacement"

    child_names = \
        ['option', 'max_vf_allowed_for_blocking', 'drag_scaling_enabled',
         'source_term_scaling_enabled']

    _child_classes = dict(
        option=option_cls,
        max_vf_allowed_for_blocking=max_vf_allowed_for_blocking_cls,
        drag_scaling_enabled=drag_scaling_enabled_cls,
        source_term_scaling_enabled=source_term_scaling_enabled_cls,
    )

    return_type = "<object object at 0x7fe5b9e4d5b0>"
