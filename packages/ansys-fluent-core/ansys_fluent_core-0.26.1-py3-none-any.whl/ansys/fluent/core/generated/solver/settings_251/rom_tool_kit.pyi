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

from .rom_data_creator_tool import rom_data_creator_tool as rom_data_creator_tool_cls
from .lti_rom_generation import lti_rom_generation as lti_rom_generation_cls

class rom_tool_kit(Group):
    fluent_name = ...
    child_names = ...
    rom_data_creator_tool: rom_data_creator_tool_cls = ...
    lti_rom_generation: lti_rom_generation_cls = ...
