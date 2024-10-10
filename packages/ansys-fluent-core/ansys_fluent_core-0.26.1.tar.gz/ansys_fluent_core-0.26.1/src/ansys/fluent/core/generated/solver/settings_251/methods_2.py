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

from .pv_coupling_controls import pv_coupling_controls as pv_coupling_controls_cls
from .pv_coupling_method import pv_coupling_method as pv_coupling_method_cls
from .gradient_controls import gradient_controls as gradient_controls_cls
from .specify_gradient_method import specify_gradient_method as specify_gradient_method_cls

class methods(Group):
    """
    Enter flexible numeris menu for solution method options.
    """

    fluent_name = "methods"

    child_names = \
        ['pv_coupling_controls', 'pv_coupling_method', 'gradient_controls',
         'specify_gradient_method']

    _child_classes = dict(
        pv_coupling_controls=pv_coupling_controls_cls,
        pv_coupling_method=pv_coupling_method_cls,
        gradient_controls=gradient_controls_cls,
        specify_gradient_method=specify_gradient_method_cls,
    )

