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

from .file_type import file_type as file_type_cls
from .file_name_1 import file_name as file_name_cls
from .pdf_file_name import pdf_file_name as pdf_file_name_cls
from .lightweight_setup import lightweight_setup as lightweight_setup_cls

class read_mesh(Command):
    fluent_name = ...
    argument_names = ...
    file_type: file_type_cls = ...
    file_name: file_name_cls = ...
    pdf_file_name: pdf_file_name_cls = ...
    lightweight_setup: lightweight_setup_cls = ...
    return_type = ...
