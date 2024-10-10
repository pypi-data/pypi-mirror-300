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

from .per_id import per_id as per_id_cls

class make_phaselag_from_periodic(Command):
    """
    Convert periodic interface to phase lagged.
    
    Parameters
    ----------
        per_id : int
            'per_id' child.
    
    """

    fluent_name = "make-phaselag-from-periodic"

    argument_names = \
        ['per_id']

    _child_classes = dict(
        per_id=per_id_cls,
    )

    return_type = "<object object at 0x7fe5b915e250>"
