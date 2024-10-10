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

from .copy_design_points import copy_design_points as copy_design_points_cls

class duplicate(Command):
    """
    Duplicate Parametric Study.
    
    Parameters
    ----------
        copy_design_points : bool
            'copy_design_points' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['copy_design_points']

    _child_classes = dict(
        copy_design_points=copy_design_points_cls,
    )

