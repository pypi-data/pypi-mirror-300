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

from .cross_section_multicomponent_child import cross_section_multicomponent_child


class cross_section_multicomponent(NamedObject[cross_section_multicomponent_child], _NonCreatableNamedObjectMixin[cross_section_multicomponent_child]):
    """
    'cross_section_multicomponent' child.
    """

    fluent_name = "cross-section-multicomponent"

    child_object_type: cross_section_multicomponent_child = cross_section_multicomponent_child
    """
    child_object_type of cross_section_multicomponent.
    """
    return_type = "<object object at 0x7ff9d14fe810>"
