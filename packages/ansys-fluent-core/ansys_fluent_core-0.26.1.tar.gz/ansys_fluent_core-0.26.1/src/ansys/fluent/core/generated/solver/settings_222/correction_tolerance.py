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

from .correction_tolerance_child import correction_tolerance_child


class correction_tolerance(NamedObject[correction_tolerance_child], CreatableNamedObjectMixinOld[correction_tolerance_child]):
    """
    'correction_tolerance' child.
    """

    fluent_name = "correction-tolerance"

    child_object_type: correction_tolerance_child = correction_tolerance_child
    """
    child_object_type of correction_tolerance.
    """
    return_type = "<object object at 0x7f82c5860a20>"
