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

from .option import option as option_cls
from .char_intrinsic_reactivity import char_intrinsic_reactivity as char_intrinsic_reactivity_cls
from .carbon_content_percentage import carbon_content_percentage as carbon_content_percentage_cls

class cbk(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    char_intrinsic_reactivity: char_intrinsic_reactivity_cls = ...
    carbon_content_percentage: carbon_content_percentage_cls = ...
    return_type = ...
