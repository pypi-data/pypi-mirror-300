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

class blottner_curve_fit(Group):
    """
    'blottner_curve_fit' child.
    """

    fluent_name = "blottner-curve-fit"

    child_names = \
        ['a', 'b', 'c']

    _child_classes = dict(
        a=a_cls,
        b=b_cls,
        c=c_cls,
    )

    return_type = "<object object at 0x7fd94caba560>"
