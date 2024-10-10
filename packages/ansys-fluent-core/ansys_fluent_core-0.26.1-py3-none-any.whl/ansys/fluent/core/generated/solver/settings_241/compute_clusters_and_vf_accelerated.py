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

from .file_name_1 import file_name as file_name_cls

class compute_clusters_and_vf_accelerated(Command):
    """
    Compute/Write surface cluster first and then view factors.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "compute-clusters-and-vf-accelerated"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

    return_type = "<object object at 0x7fd94d0e4510>"
