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

from .file_name import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls

class write_sc_file(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    overwrite: overwrite_cls = ...
    return_type = ...
