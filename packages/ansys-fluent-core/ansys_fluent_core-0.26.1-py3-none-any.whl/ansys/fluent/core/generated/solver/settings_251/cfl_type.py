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


class cfl_type(String, AllowedValuesMixin):
    """
    Set CFL type 
    [1]Convective   [2]Convective-Diffusive   [3]Acoustic   [4]Flow.
    """

    fluent_name = "cfl-type"

