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


class degassing_verbosity(Integer, AllowedValuesMixin):
    """
    Set the verbosity level of the total mass flow rate at the degassing boundary. The acceptable values are:
      0 - off
      1 - report per time step.
    """

    fluent_name = "degassing-verbosity"

