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

from .sub_time_step_method import sub_time_step_method as sub_time_step_method_cls
from .solve_vof_every_iter import solve_vof_every_iter as solve_vof_every_iter_cls
from .vof_filtering import vof_filtering as vof_filtering_cls

class explicit_expert_options(Group):
    """
    Explicit expert options.
    """

    fluent_name = "explicit-expert-options"

    child_names = \
        ['sub_time_step_method', 'solve_vof_every_iter', 'vof_filtering']

    _child_classes = dict(
        sub_time_step_method=sub_time_step_method_cls,
        solve_vof_every_iter=solve_vof_every_iter_cls,
        vof_filtering=vof_filtering_cls,
    )

