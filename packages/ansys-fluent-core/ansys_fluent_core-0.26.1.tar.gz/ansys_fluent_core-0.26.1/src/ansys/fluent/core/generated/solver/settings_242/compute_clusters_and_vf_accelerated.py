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

from .file_name_6 import file_name as file_name_cls

class compute_clusters_and_vf_accelerated(Command):
    """
    Compute and write both surface clusters and view factors with GPU-acceleration.
    
    Parameters
    ----------
        file_name : str
            Name of output file for updated surface clusters and view factors with GPU-acceleration.
    
    """

    fluent_name = "compute-clusters-and-vf-accelerated"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

