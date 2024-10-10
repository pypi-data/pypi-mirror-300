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

from .model_1 import model as model_cls
from .solar_load import solar_load as solar_load_cls
from .discrete_ordinates import discrete_ordinates as discrete_ordinates_cls
from .monte_carlo import monte_carlo as monte_carlo_cls
from .s2s import s2s as s2s_cls
from .multiband import multiband as multiband_cls
from .solve_frequency import solve_frequency as solve_frequency_cls

class radiation(Group):
    """
    'radiation' child.
    """

    fluent_name = "radiation"

    child_names = \
        ['model', 'solar_load', 'discrete_ordinates', 'monte_carlo', 's2s',
         'multiband', 'solve_frequency']

    _child_classes = dict(
        model=model_cls,
        solar_load=solar_load_cls,
        discrete_ordinates=discrete_ordinates_cls,
        monte_carlo=monte_carlo_cls,
        s2s=s2s_cls,
        multiband=multiband_cls,
        solve_frequency=solve_frequency_cls,
    )

    return_type = "<object object at 0x7fe5bb500f90>"
