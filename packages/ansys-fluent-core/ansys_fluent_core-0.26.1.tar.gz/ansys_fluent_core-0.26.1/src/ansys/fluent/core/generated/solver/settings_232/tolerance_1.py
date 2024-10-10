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

from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .tolerance1 import tolerance1 as tolerance1_cls
from .tolerance2 import tolerance2 as tolerance2_cls
from .update import update as update_cls

class tolerance(Command):
    """
    Specification of mapped interface tolerance.
    
    Parameters
    ----------
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        tolerance1 : real
            'tolerance1' child.
        tolerance2 : real
            'tolerance2' child.
        update : bool
            Update mapped interface with new tolerance.
    
    """

    fluent_name = "tolerance"

    argument_names = \
        ['use_local_edge_length_factor', 'tolerance1', 'tolerance2', 'update']

    _child_classes = dict(
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        tolerance1=tolerance1_cls,
        tolerance2=tolerance2_cls,
        update=update_cls,
    )

    return_type = "<object object at 0x7fe5b915e0a0>"
