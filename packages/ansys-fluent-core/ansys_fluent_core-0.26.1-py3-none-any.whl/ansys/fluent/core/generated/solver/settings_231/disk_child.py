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

from .general_1 import general as general_cls
from .geometry_1 import geometry as geometry_cls
from .trimming import trimming as trimming_cls

class disk_child(Group):
    """
    'child_object_type' of disk.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['general', 'geometry', 'trimming']

    _child_classes = dict(
        general=general_cls,
        geometry=geometry_cls,
        trimming=trimming_cls,
    )

    return_type = "<object object at 0x7ff9d13700d0>"
