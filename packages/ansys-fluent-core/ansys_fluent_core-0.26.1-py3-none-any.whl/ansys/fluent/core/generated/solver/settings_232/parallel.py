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

from .option_5 import option as option_cls
from .expert_options import expert_options as expert_options_cls
from .hybrid_options import hybrid_options as hybrid_options_cls

class parallel(Group):
    """
    Main menu to allow users to set options controlling the parallel scheme used when tracking particles. 
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "parallel"

    child_names = \
        ['option', 'expert_options', 'hybrid_options']

    _child_classes = dict(
        option=option_cls,
        expert_options=expert_options_cls,
        hybrid_options=hybrid_options_cls,
    )

    return_type = "<object object at 0x7fe5b9e4d510>"
