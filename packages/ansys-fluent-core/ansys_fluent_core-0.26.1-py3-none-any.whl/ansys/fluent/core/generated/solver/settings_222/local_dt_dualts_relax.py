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

from .relaxation_factor_child import relaxation_factor_child


class local_dt_dualts_relax(NamedObject[relaxation_factor_child], CreatableNamedObjectMixinOld[relaxation_factor_child]):
    """
    'local_dt_dualts_relax' child.
    """

    fluent_name = "local-dt-dualts-relax"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of local_dt_dualts_relax.
    """
    return_type = "<object object at 0x7f82c5861e90>"
