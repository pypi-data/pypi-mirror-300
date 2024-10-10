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

from .generic import generic as generic_cls
from .finnie import finnie as finnie_cls
from .mclaury import mclaury as mclaury_cls
from .oka import oka as oka_cls
from .dnv import dnv as dnv_cls
from .shear_erosion import shear_erosion as shear_erosion_cls

class erosion(Group):
    fluent_name = ...
    child_names = ...
    generic: generic_cls = ...
    finnie: finnie_cls = ...
    mclaury: mclaury_cls = ...
    oka: oka_cls = ...
    dnv: dnv_cls = ...
    shear_erosion: shear_erosion_cls = ...
