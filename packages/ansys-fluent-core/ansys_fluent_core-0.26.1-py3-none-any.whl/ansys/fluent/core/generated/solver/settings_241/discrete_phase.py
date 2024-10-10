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

from .general_settings import general_settings as general_settings_cls
from .injections import injections as injections_cls
from .numerics import numerics as numerics_cls
from .parallel import parallel as parallel_cls
from .physical_models_1 import physical_models as physical_models_cls
from .tracking_1 import tracking as tracking_cls
from .user_functions import user_functions as user_functions_cls

class discrete_phase(Group):
    """
    Toplevel menu of the Discrete Phase multiphase model. A discrete phase model (DPM) is used when the aim is to investigate the behavior of the particles from a Lagrangian view and a discrete perspective.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['general_settings', 'injections', 'numerics', 'parallel',
         'physical_models', 'tracking', 'user_functions']

    _child_classes = dict(
        general_settings=general_settings_cls,
        injections=injections_cls,
        numerics=numerics_cls,
        parallel=parallel_cls,
        physical_models=physical_models_cls,
        tracking=tracking_cls,
        user_functions=user_functions_cls,
    )

    return_type = "<object object at 0x7fd94d0e6340>"
