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

from typing import Union, List, Tuple

from .solution_stabilization_1 import solution_stabilization as solution_stabilization_cls
from .verbosity_10 import verbosity as verbosity_cls
from .parameters_2 import parameters as parameters_cls
from .spatial import spatial as spatial_cls
from .transient import transient as transient_cls
from .amg import amg as amg_cls
from .models_2 import models as models_cls
from .methods_1 import methods as methods_cls
from .miscellaneous import miscellaneous as miscellaneous_cls
from .set_settings_to_default import set_settings_to_default as set_settings_to_default_cls

class contact_solution_controls(Group):
    fluent_name = ...
    child_names = ...
    solution_stabilization: solution_stabilization_cls = ...
    verbosity: verbosity_cls = ...
    parameters: parameters_cls = ...
    spatial: spatial_cls = ...
    transient: transient_cls = ...
    amg: amg_cls = ...
    models: models_cls = ...
    methods: methods_cls = ...
    miscellaneous: miscellaneous_cls = ...
    command_names = ...

    def set_settings_to_default(self, ):
        """
        Set contact solution stabilization to default.
        """

