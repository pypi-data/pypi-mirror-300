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

from .sigma import sigma as sigma_cls
from .sigma2 import sigma2 as sigma2_cls
from .relax import relax as relax_cls
from .tangential_source import tangential_source as tangential_source_cls
from .verbosity_4 import verbosity as verbosity_cls

class general_nrbc(Group):
    fluent_name = ...
    child_names = ...
    sigma: sigma_cls = ...
    sigma2: sigma2_cls = ...
    relax: relax_cls = ...
    tangential_source: tangential_source_cls = ...
    verbosity: verbosity_cls = ...
    return_type = ...
