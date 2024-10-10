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

from .path_1 import path_1 as path_1_cls
from .filename import filename as filename_cls
from .extension import extension as extension_cls

class outline_view_settings(Command):
    fluent_name = ...
    argument_names = ...
    path_1: path_1_cls = ...
    filename: filename_cls = ...
    extension: extension_cls = ...
