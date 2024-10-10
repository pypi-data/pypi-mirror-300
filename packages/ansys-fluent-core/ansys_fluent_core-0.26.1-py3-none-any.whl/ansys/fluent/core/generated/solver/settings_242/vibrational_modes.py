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

from .vibrational_temperature_mode_1 import vibrational_temperature_mode_1 as vibrational_temperature_mode_1_cls
from .vibrational_degeneracy_mode_1 import vibrational_degeneracy_mode_1 as vibrational_degeneracy_mode_1_cls
from .vibrational_temperature_mode_2 import vibrational_temperature_mode_2 as vibrational_temperature_mode_2_cls
from .vibrational_degeneracy_mode_2 import vibrational_degeneracy_mode_2 as vibrational_degeneracy_mode_2_cls
from .vibrational_temperature_mode_3 import vibrational_temperature_mode_3 as vibrational_temperature_mode_3_cls
from .vibrational_degeneracy_mode_3 import vibrational_degeneracy_mode_3 as vibrational_degeneracy_mode_3_cls

class vibrational_modes(Group):
    """
    Vibrational modes settings.
    """

    fluent_name = "vibrational-modes"

    child_names = \
        ['vibrational_temperature_mode_1', 'vibrational_degeneracy_mode_1',
         'vibrational_temperature_mode_2', 'vibrational_degeneracy_mode_2',
         'vibrational_temperature_mode_3', 'vibrational_degeneracy_mode_3']

    _child_classes = dict(
        vibrational_temperature_mode_1=vibrational_temperature_mode_1_cls,
        vibrational_degeneracy_mode_1=vibrational_degeneracy_mode_1_cls,
        vibrational_temperature_mode_2=vibrational_temperature_mode_2_cls,
        vibrational_degeneracy_mode_2=vibrational_degeneracy_mode_2_cls,
        vibrational_temperature_mode_3=vibrational_temperature_mode_3_cls,
        vibrational_degeneracy_mode_3=vibrational_degeneracy_mode_3_cls,
    )

