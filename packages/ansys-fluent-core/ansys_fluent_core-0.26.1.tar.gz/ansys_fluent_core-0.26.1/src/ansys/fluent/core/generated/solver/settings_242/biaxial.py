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

from .planar_conductivity import planar_conductivity as planar_conductivity_cls
from .transverse_conductivity import transverse_conductivity as transverse_conductivity_cls

class biaxial(Group):
    """
    Biaxial orthotropic conductivity settings.
    """

    fluent_name = "biaxial"

    child_names = \
        ['planar_conductivity', 'transverse_conductivity']

    _child_classes = dict(
        planar_conductivity=planar_conductivity_cls,
        transverse_conductivity=transverse_conductivity_cls,
    )

