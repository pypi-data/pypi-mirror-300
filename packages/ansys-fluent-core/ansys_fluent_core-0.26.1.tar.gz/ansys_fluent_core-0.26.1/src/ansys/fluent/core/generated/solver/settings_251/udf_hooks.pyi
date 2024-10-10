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

from .ntgk_model_parameter import ntgk_model_parameter as ntgk_model_parameter_cls
from .ecm_model_parameter import ecm_model_parameter as ecm_model_parameter_cls
from .user_defined_echem_model import user_defined_echem_model as user_defined_echem_model_cls
from .p2d_bv_rate import p2d_bv_rate as p2d_bv_rate_cls
from .p2d_postprocessing import p2d_postprocessing as p2d_postprocessing_cls
from .p2d_porosity_p import p2d_porosity_p as p2d_porosity_p_cls
from .p2d_porosity_n import p2d_porosity_n as p2d_porosity_n_cls

class udf_hooks(Group):
    fluent_name = ...
    child_names = ...
    ntgk_model_parameter: ntgk_model_parameter_cls = ...
    ecm_model_parameter: ecm_model_parameter_cls = ...
    user_defined_echem_model: user_defined_echem_model_cls = ...
    p2d_bv_rate: p2d_bv_rate_cls = ...
    p2d_postprocessing: p2d_postprocessing_cls = ...
    p2d_porosity_p: p2d_porosity_p_cls = ...
    p2d_porosity_n: p2d_porosity_n_cls = ...
