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

from .field_7 import field as field_cls
from .scalefactor_1 import scalefactor as scalefactor_cls

class ribbon_settings(Group):
    """
    Change ribbon field and scale factor.
    """

    fluent_name = "ribbon-settings"

    child_names = \
        ['field', 'scalefactor']

    _child_classes = dict(
        field=field_cls,
        scalefactor=scalefactor_cls,
    )

