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

from .user_specified_species import user_specified_species as user_specified_species_cls
from .species_11 import species as species_cls

class species_setting(Group):
    fluent_name = ...
    child_names = ...
    user_specified_species: user_specified_species_cls = ...
    species: species_cls = ...
    return_type = ...
