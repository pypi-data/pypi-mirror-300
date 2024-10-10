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

from .polar_real_angle import polar_real_angle as polar_real_angle_cls
from .polar_real_intensity import polar_real_intensity as polar_real_intensity_cls

class polar_data_pairs_child(Group):
    """
    'child_object_type' of polar_data_pairs.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['polar_real_angle', 'polar_real_intensity']

    _child_classes = dict(
        polar_real_angle=polar_real_angle_cls,
        polar_real_intensity=polar_real_intensity_cls,
    )

