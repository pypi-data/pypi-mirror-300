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

from .sbes_sdes_hybrid_model_optn import sbes_sdes_hybrid_model_optn as sbes_sdes_hybrid_model_optn_cls
from .user_defined_1 import user_defined as user_defined_cls

class sbes_sdes_hybrid_model(Group):
    fluent_name = ...
    child_names = ...
    sbes_sdes_hybrid_model_optn: sbes_sdes_hybrid_model_optn_cls = ...
    user_defined: user_defined_cls = ...
    return_type = ...
