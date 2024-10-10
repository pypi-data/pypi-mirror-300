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

from .matrix_component import matrix_component as matrix_component_cls
from .conductivity import conductivity as conductivity_cls

class anisotropic(Group):
    """
    Anisotropic orthotropic conductivity settings.
    """

    fluent_name = "anisotropic"

    child_names = \
        ['matrix_component', 'conductivity']

    _child_classes = dict(
        matrix_component=matrix_component_cls,
        conductivity=conductivity_cls,
    )

