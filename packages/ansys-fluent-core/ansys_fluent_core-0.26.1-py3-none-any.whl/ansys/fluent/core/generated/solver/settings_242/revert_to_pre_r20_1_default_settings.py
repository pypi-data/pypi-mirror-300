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

from .old_default_of_operating_density_method import old_default_of_operating_density_method as old_default_of_operating_density_method_cls
from .old_default_of_volume_fraction_smoothing import old_default_of_volume_fraction_smoothing as old_default_of_volume_fraction_smoothing_cls
from .old_variant_of_pesto_for_cases_using_structured_mesh import old_variant_of_pesto_for_cases_using_structured_mesh as old_variant_of_pesto_for_cases_using_structured_mesh_cls

class revert_to_pre_r20_1_default_settings(Group):
    """
    Revert to pre-R20.1 multiphase flow default settings.
    """

    fluent_name = "revert-to-pre-r20-1-default-settings?"

    child_names = \
        ['old_default_of_operating_density_method',
         'old_default_of_volume_fraction_smoothing',
         'old_variant_of_pesto_for_cases_using_structured_mesh']

    _child_classes = dict(
        old_default_of_operating_density_method=old_default_of_operating_density_method_cls,
        old_default_of_volume_fraction_smoothing=old_default_of_volume_fraction_smoothing_cls,
        old_variant_of_pesto_for_cases_using_structured_mesh=old_variant_of_pesto_for_cases_using_structured_mesh_cls,
    )

