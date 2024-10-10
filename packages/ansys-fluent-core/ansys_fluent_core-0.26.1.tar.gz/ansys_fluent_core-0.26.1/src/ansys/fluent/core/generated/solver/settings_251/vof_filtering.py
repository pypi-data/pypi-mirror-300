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

from .enable_vof_filtering import enable_vof_filtering as enable_vof_filtering_cls
from .filtering_options import filtering_options as filtering_options_cls
from .filter_vof_cutoff import filter_vof_cutoff as filter_vof_cutoff_cls

class vof_filtering(Group):
    """
    Vof-filtering-class.
    """

    fluent_name = "vof-filtering"

    child_names = \
        ['enable_vof_filtering', 'filtering_options', 'filter_vof_cutoff']

    _child_classes = dict(
        enable_vof_filtering=enable_vof_filtering_cls,
        filtering_options=filtering_options_cls,
        filter_vof_cutoff=filter_vof_cutoff_cls,
    )

