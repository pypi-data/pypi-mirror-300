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

from .les_spec_name import les_spec_name as les_spec_name_cls
from .rfg_number_of_modes import rfg_number_of_modes as rfg_number_of_modes_cls
from .vm_nvortices import vm_nvortices as vm_nvortices_cls
from .les_embedded_fluctuations import les_embedded_fluctuations as les_embedded_fluctuations_cls

class turbulence(Group):
    fluent_name = ...
    child_names = ...
    les_spec_name: les_spec_name_cls = ...
    rfg_number_of_modes: rfg_number_of_modes_cls = ...
    vm_nvortices: vm_nvortices_cls = ...
    les_embedded_fluctuations: les_embedded_fluctuations_cls = ...
