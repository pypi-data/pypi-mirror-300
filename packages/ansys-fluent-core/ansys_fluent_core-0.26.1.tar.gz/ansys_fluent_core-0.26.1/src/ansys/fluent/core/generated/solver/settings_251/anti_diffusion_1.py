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

from .enable_dynamic_strength import enable_dynamic_strength as enable_dynamic_strength_cls
from .set_dynamic_strength_exponent import set_dynamic_strength_exponent as set_dynamic_strength_exponent_cls
from .set_maximum_dynamic_strength import set_maximum_dynamic_strength as set_maximum_dynamic_strength_cls

class anti_diffusion(Group):
    """
    Anti Diffusion Menu for VOF/Multi-Fluid VOF Models.
    """

    fluent_name = "anti-diffusion"

    child_names = \
        ['enable_dynamic_strength', 'set_dynamic_strength_exponent',
         'set_maximum_dynamic_strength']

    _child_classes = dict(
        enable_dynamic_strength=enable_dynamic_strength_cls,
        set_dynamic_strength_exponent=set_dynamic_strength_exponent_cls,
        set_maximum_dynamic_strength=set_maximum_dynamic_strength_cls,
    )

