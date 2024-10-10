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
from .combusting_particle_child import combusting_particle_child


class combusting_particle(NamedObject[combusting_particle_child], CreatableNamedObjectMixinOld[combusting_particle_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: combusting_particle_child = combusting_particle_child
    """
    child_object_type of combusting_particle.
    """
    return_type = "<object object at 0x7fe5ba527290>"
