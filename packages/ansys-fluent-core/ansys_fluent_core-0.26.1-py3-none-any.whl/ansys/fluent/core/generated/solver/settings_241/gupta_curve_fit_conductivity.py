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

from .a_1 import a as a_cls
from .b import b as b_cls
from .c import c as c_cls
from .d import d as d_cls
from .e_1 import e as e_cls

class gupta_curve_fit_conductivity(Group):
    """
    'gupta_curve_fit_conductivity' child.
    """

    fluent_name = "gupta-curve-fit-conductivity"

    child_names = \
        ['a', 'b', 'c', 'd', 'e']

    _child_classes = dict(
        a=a_cls,
        b=b_cls,
        c=c_cls,
        d=d_cls,
        e=e_cls,
    )

    return_type = "<object object at 0x7fd94cabad30>"
