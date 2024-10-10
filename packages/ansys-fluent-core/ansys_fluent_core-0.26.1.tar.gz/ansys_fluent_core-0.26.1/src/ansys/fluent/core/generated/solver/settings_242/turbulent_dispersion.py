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

from .enabled_14 import enabled as enabled_cls
from .option_11 import option as option_cls
from .random_eddy_lifetime import random_eddy_lifetime as random_eddy_lifetime_cls
from .number_of_tries import number_of_tries as number_of_tries_cls
from .time_scale_constant_1 import time_scale_constant as time_scale_constant_cls
from .length_scale_constant import length_scale_constant as length_scale_constant_cls

class turbulent_dispersion(Group):
    """
    'turbulent_dispersion' child.
    """

    fluent_name = "turbulent-dispersion"

    child_names = \
        ['enabled', 'option', 'random_eddy_lifetime', 'number_of_tries',
         'time_scale_constant', 'length_scale_constant']

    _child_classes = dict(
        enabled=enabled_cls,
        option=option_cls,
        random_eddy_lifetime=random_eddy_lifetime_cls,
        number_of_tries=number_of_tries_cls,
        time_scale_constant=time_scale_constant_cls,
        length_scale_constant=length_scale_constant_cls,
    )

