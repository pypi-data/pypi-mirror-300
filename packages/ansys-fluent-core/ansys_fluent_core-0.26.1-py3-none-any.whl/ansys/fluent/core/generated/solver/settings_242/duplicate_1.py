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

from .design_point import design_point as design_point_cls

class duplicate(Command):
    """
    Duplicate Design Point.
    
    Parameters
    ----------
        design_point : str
            'design_point' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['design_point']

    _child_classes = dict(
        design_point=design_point_cls,
    )

