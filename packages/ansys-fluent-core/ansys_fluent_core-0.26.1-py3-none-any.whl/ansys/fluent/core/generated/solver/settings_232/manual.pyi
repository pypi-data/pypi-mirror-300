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

from typing import Union, List, Tuple

from .faces_2 import faces as faces_cls
from .edges_2 import edges as edges_cls
from .nodes_1 import nodes as nodes_cls
from .material_color import material_color as material_color_cls

class manual(Group):
    fluent_name = ...
    child_names = ...
    faces: faces_cls = ...
    edges: edges_cls = ...
    nodes: nodes_cls = ...
    material_color: material_color_cls = ...
    return_type = ...
