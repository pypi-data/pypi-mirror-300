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

from .enabled_12 import enabled as enabled_cls
from .model_type import model_type as model_type_cls
from .only_abuse import only_abuse as only_abuse_cls
from .one_equation import one_equation as one_equation_cls
from .four_equation import four_equation as four_equation_cls
from .internal_short import internal_short as internal_short_cls

class thermal_abuse_model(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    model_type: model_type_cls = ...
    only_abuse: only_abuse_cls = ...
    one_equation: one_equation_cls = ...
    four_equation: four_equation_cls = ...
    internal_short: internal_short_cls = ...
    return_type = ...
