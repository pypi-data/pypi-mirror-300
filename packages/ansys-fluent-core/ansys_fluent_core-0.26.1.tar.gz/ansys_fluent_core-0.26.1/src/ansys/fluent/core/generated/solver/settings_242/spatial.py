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

from .first_to_second_order_blending_1 import first_to_second_order_blending as first_to_second_order_blending_cls
from .first_to_second_order_blending_list import first_to_second_order_blending_list as first_to_second_order_blending_list_cls
from .scheme import scheme as scheme_cls
from .flow_skew_diffusion_exclude import flow_skew_diffusion_exclude as flow_skew_diffusion_exclude_cls
from .scalars_skew_diffusion_exclude import scalars_skew_diffusion_exclude as scalars_skew_diffusion_exclude_cls
from .rhie_chow_flux_specify import rhie_chow_flux_specify as rhie_chow_flux_specify_cls
from .rhie_chow_method import rhie_chow_method as rhie_chow_method_cls

class spatial(Group):
    """
    Enter flexible numeris menu for spatial discretization options.
    """

    fluent_name = "spatial"

    child_names = \
        ['first_to_second_order_blending',
         'first_to_second_order_blending_list', 'scheme',
         'flow_skew_diffusion_exclude', 'scalars_skew_diffusion_exclude',
         'rhie_chow_flux_specify', 'rhie_chow_method']

    _child_classes = dict(
        first_to_second_order_blending=first_to_second_order_blending_cls,
        first_to_second_order_blending_list=first_to_second_order_blending_list_cls,
        scheme=scheme_cls,
        flow_skew_diffusion_exclude=flow_skew_diffusion_exclude_cls,
        scalars_skew_diffusion_exclude=scalars_skew_diffusion_exclude_cls,
        rhie_chow_flux_specify=rhie_chow_flux_specify_cls,
        rhie_chow_method=rhie_chow_method_cls,
    )

