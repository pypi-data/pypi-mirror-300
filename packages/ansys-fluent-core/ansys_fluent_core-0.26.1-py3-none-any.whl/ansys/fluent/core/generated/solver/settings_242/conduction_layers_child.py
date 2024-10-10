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

from .thickness import thickness as thickness_cls
from .material_5 import material as material_cls
from .qdot import qdot as qdot_cls

class conduction_layers_child(Group):
    """
    'child_object_type' of conduction_layers.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thickness', 'material', 'qdot']

    _child_classes = dict(
        thickness=thickness_cls,
        material=material_cls,
        qdot=qdot_cls,
    )

