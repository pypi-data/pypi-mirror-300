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

from .all import all as all_cls
from .auto import auto as auto_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .tolerance1 import tolerance1 as tolerance1_cls
from .tolerance2 import tolerance2 as tolerance2_cls

class convert_to_mapped_interface(Command):
    """
    Convert non-conformal mesh interface to mapped mesh interfaces.
    
    Parameters
    ----------
        all : bool
            Convert all mesh interfaces to mapped mesh interfaces.
        auto : bool
            Convert poorly matching mesh interfaces to mapped mesh interfaces.
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        tolerance1 : real
            'tolerance1' child.
        tolerance2 : real
            'tolerance2' child.
    
    """

    fluent_name = "convert-to-mapped-interface"

    argument_names = \
        ['all', 'auto', 'use_local_edge_length_factor', 'tolerance1',
         'tolerance2']

    _child_classes = dict(
        all=all_cls,
        auto=auto_cls,
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        tolerance1=tolerance1_cls,
        tolerance2=tolerance2_cls,
    )

    return_type = "<object object at 0x7fe5b915e100>"
