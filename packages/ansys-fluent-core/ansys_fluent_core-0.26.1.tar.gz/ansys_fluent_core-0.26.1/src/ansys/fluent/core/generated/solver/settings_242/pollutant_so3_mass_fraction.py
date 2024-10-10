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

from .option_17 import option as option_cls
from .value_13 import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls

class pollutant_so3_mass_fraction(Group):
    """
    Specify Pollutant SO3 Mass Fraction.
    """

    fluent_name = "pollutant-so3-mass-fraction"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        profile_name=profile_name_cls,
        field_name=field_name_cls,
        udf=udf_cls,
    )

    _child_aliases = dict(
        constant="value",
    )

