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

from .f_length import f_length as f_length_cls
from .re_theta_c import re_theta_c as re_theta_c_cls
from .re_theta_t import re_theta_t as re_theta_t_cls

class user_defined_transition(Group):
    fluent_name = ...
    child_names = ...
    f_length: f_length_cls = ...
    re_theta_c: re_theta_c_cls = ...
    re_theta_t: re_theta_t_cls = ...
    return_type = ...
