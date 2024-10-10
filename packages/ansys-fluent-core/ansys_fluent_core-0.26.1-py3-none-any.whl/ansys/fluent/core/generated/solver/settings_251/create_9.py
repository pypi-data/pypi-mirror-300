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

from .coefficients_2 import coefficients as coefficients_cls
from .distance import distance as distance_cls

class create(CommandWithPositionalArgs):
    """
    To define a mirror plane for a non-symmetric domain.
    
    Parameters
    ----------
        coefficients : List
            Set the cofficients of X, Y and Z.
        distance : real
            Set the distance of the plane from the origin.
    
    """

    fluent_name = "create"

    argument_names = \
        ['coefficients', 'distance']

    _child_classes = dict(
        coefficients=coefficients_cls,
        distance=distance_cls,
    )

