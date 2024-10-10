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

from .implicit_body_force import implicit_body_force as implicit_body_force_cls
from .explicit_expert_options import explicit_expert_options as explicit_expert_options_cls

class advanced_formulation(Group):
    """
    Set body force formulation.
    """

    fluent_name = "advanced-formulation"

    child_names = \
        ['implicit_body_force', 'explicit_expert_options']

    _child_classes = dict(
        implicit_body_force=implicit_body_force_cls,
        explicit_expert_options=explicit_expert_options_cls,
    )

