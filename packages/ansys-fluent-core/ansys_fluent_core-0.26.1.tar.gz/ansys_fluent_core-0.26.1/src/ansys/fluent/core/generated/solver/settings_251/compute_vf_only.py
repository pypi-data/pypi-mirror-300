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

from .file_name_7 import file_name as file_name_cls

class compute_vf_only(Command):
    """
    Compute and write only view factors from existing surface clusters.
    
    Parameters
    ----------
        file_name : str
            Name of output file for S2S view factors from existing surface clusters.
    
    """

    fluent_name = "compute-vf-only"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

