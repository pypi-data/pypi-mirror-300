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


class include_in_domain_particles(Boolean):
    """
    Specify whether to include particle parcels that are currently in the domain in the report.
    This may take some extra time for the report to be prepared.
    """

    fluent_name = "include-in-domain-particles?"

