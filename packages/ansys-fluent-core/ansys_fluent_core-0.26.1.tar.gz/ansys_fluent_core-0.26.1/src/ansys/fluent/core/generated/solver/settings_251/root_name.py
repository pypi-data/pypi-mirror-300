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


class root_name(Filename, _OutputFile):
    """
    Set the root name for auto-saved files. The number of iterations or time steps will be appended to this root name.
    """

    fluent_name = "root-name"

