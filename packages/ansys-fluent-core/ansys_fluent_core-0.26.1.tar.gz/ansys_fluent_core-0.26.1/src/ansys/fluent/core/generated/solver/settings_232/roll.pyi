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

from .counter_clockwise import counter_clockwise as counter_clockwise_cls

class roll(Command):
    fluent_name = ...
    argument_names = ...
    counter_clockwise: counter_clockwise_cls = ...
    return_type = ...
