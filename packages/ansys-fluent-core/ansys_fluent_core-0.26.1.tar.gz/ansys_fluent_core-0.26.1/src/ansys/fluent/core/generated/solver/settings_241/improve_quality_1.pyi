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

from .check_mapped_interface_quality import check_mapped_interface_quality as check_mapped_interface_quality_cls
from .continue_ import continue_ as continue__cls
from .tol_percentage_increment import tol_percentage_increment as tol_percentage_increment_cls

class improve_quality(Command):
    fluent_name = ...
    argument_names = ...
    check_mapped_interface_quality: check_mapped_interface_quality_cls = ...
    continue_: continue__cls = ...
    tol_percentage_increment: tol_percentage_increment_cls = ...
    return_type = ...
