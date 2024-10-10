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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .set_damping_strengths_child import set_damping_strengths_child


class local_dt_dualts_relax(NamedObject[set_damping_strengths_child], _NonCreatableNamedObjectMixin[set_damping_strengths_child]):
    """
    'local_dt_dualts_relax' child.
    """

    fluent_name = "local-dt-dualts-relax"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: set_damping_strengths_child = set_damping_strengths_child
    """
    child_object_type of local_dt_dualts_relax.
    """
    return_type = "<object object at 0x7fe5b9058150>"
