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


class injection_names(StringList, AllowedValuesMixin):
    """
    Specify the injection[s] whose in-domain particle parcels are to be included in the report.
    """

    fluent_name = "injection-names"

