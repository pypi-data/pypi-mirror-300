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

from .enable_14 import enable as enable_cls
from .discretization import discretization as discretization_cls
from .under_relaxation_1 import under_relaxation as under_relaxation_cls
from .verbosity_5 import verbosity as verbosity_cls
from .initialize import initialize as initialize_cls
from .show_status import show_status as show_status_cls

class turbo_sepcific_nrbc(Group):
    """
    Enter the turbo-specific n.r.b.c. menu.
    """

    fluent_name = "turbo-sepcific-nrbc"

    child_names = \
        ['enable', 'discretization', 'under_relaxation', 'verbosity']

    command_names = \
        ['initialize', 'show_status']

    _child_classes = dict(
        enable=enable_cls,
        discretization=discretization_cls,
        under_relaxation=under_relaxation_cls,
        verbosity=verbosity_cls,
        initialize=initialize_cls,
        show_status=show_status_cls,
    )

