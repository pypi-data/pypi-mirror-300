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

from .model import model as model_cls
from .options_4 import options as options_cls
from .controls import controls as controls_cls
from .expert import expert as expert_cls

class structure(Group):
    """
    'structure' child.
    """

    fluent_name = "structure"

    child_names = \
        ['model', 'options', 'controls', 'expert']

    _child_classes = dict(
        model=model_cls,
        options=options_cls,
        controls=controls_cls,
        expert=expert_cls,
    )

    return_type = "<object object at 0x7fe5b9e4e180>"
