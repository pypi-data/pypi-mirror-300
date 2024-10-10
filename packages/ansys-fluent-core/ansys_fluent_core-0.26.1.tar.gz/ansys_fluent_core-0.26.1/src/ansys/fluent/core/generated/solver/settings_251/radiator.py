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

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .loss_coefficient import loss_coefficient as loss_coefficient_cls
from .hc import hc as hc_cls
from .t import t as t_cls
from .heat_flux import heat_flux as heat_flux_cls
from .strength import strength as strength_cls

class radiator(Group):
    """
    Allows to change radiator model variables or settings.
    """

    fluent_name = "radiator"

    child_names = \
        ['porous_jump_turb_wall_treatment', 'loss_coefficient', 'hc', 't',
         'heat_flux', 'strength']

    _child_classes = dict(
        porous_jump_turb_wall_treatment=porous_jump_turb_wall_treatment_cls,
        loss_coefficient=loss_coefficient_cls,
        hc=hc_cls,
        t=t_cls,
        heat_flux=heat_flux_cls,
        strength=strength_cls,
    )

    _child_aliases = dict(
        kc="loss_coefficient",
        q="heat_flux",
    )

