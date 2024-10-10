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

from .ra import ra as ra_cls
from .rz import rz as rz_cls
from .rq import rq as rq_cls
from .rsm import rsm as rsm_cls

class wall_roughness_parameters(Group):
    """
    Wall roughness parameters.
    """

    fluent_name = "wall-roughness-parameters"

    child_names = \
        ['ra', 'rz', 'rq', 'rsm']

    _child_classes = dict(
        ra=ra_cls,
        rz=rz_cls,
        rq=rq_cls,
        rsm=rsm_cls,
    )

    _child_aliases = dict(
        dpm_ra_roughness="ra",
        dpm_rq_roughness="rq",
        dpm_rsm_roughness="rsm",
        dpm_rz_roughness="rz",
    )

