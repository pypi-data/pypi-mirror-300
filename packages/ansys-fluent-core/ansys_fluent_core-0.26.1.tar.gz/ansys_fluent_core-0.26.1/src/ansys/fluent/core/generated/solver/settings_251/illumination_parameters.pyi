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

from .direct_solar_irradiation import direct_solar_irradiation as direct_solar_irradiation_cls
from .diffuse_solar_irradiation import diffuse_solar_irradiation as diffuse_solar_irradiation_cls
from .spectral_fraction import spectral_fraction as spectral_fraction_cls

class illumination_parameters(Group):
    fluent_name = ...
    child_names = ...
    direct_solar_irradiation: direct_solar_irradiation_cls = ...
    diffuse_solar_irradiation: diffuse_solar_irradiation_cls = ...
    spectral_fraction: spectral_fraction_cls = ...
