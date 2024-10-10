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

from .sb0 import sb0 as sb0_cls
from .sb1 import sb1 as sb1_cls
from .angle import angle as angle_cls
from .pl_name import pl_name as pl_name_cls

class make_phaselag_from_boundaries(Command):
    """
    Make interface zones phase lagged.
    
    Parameters
    ----------
        sb0 : int
            Enter id/name of zone to convert to phase lag side 1.
        sb1 : int
            Enter id/name of zone to convert to phase lag side 2.
        angle : real
            'angle' child.
        pl_name : str
            'pl_name' child.
    
    """

    fluent_name = "make-phaselag-from-boundaries"

    argument_names = \
        ['sb0', 'sb1', 'angle', 'pl_name']

    _child_classes = dict(
        sb0=sb0_cls,
        sb1=sb1_cls,
        angle=angle_cls,
        pl_name=pl_name_cls,
    )

    return_type = "<object object at 0x7fe5b915e220>"
