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

from .option_3 import option as option_cls
from .smooth import smooth as smooth_cls
from .banded import banded as banded_cls

class coloring(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    smooth: smooth_cls = ...
    banded: banded_cls = ...
    return_type = ...
