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

from .file_suffix_type import file_suffix_type as file_suffix_type_cls
from .file_decimal_digit import file_decimal_digit as file_decimal_digit_cls

class append_file_name_with(Group):
    """
    Set the suffix for auto-saved files. The file name can be appended by flow-time, time-step value or by user specified flags in file name.
    """

    fluent_name = "append-file-name-with"

    child_names = \
        ['file_suffix_type', 'file_decimal_digit']

    _child_classes = dict(
        file_suffix_type=file_suffix_type_cls,
        file_decimal_digit=file_decimal_digit_cls,
    )

