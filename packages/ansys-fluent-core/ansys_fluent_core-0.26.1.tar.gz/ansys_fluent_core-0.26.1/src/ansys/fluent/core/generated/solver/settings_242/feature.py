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

from .feature_angle import feature_angle as feature_angle_cls

class feature(Group):
    """
    Enables feature lines in an outline display.
    """

    fluent_name = "feature"

    child_names = \
        ['feature_angle']

    _child_classes = dict(
        feature_angle=feature_angle_cls,
    )

