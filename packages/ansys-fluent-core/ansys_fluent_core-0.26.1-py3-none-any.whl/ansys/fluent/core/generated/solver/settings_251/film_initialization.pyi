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

from .enabled_41 import enabled as enabled_cls
from .film_height import film_height as film_height_cls
from .film_velocity import film_velocity as film_velocity_cls
from .film_temperature import film_temperature as film_temperature_cls
from .injection import injection as injection_cls
from .min_parcels_per_unit_area import min_parcels_per_unit_area as min_parcels_per_unit_area_cls
from .min_parcels_per_facet import min_parcels_per_facet as min_parcels_per_facet_cls
from .do_initialization_now import do_initialization_now as do_initialization_now_cls

class film_initialization(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    film_height: film_height_cls = ...
    film_velocity: film_velocity_cls = ...
    film_temperature: film_temperature_cls = ...
    injection: injection_cls = ...
    min_parcels_per_unit_area: min_parcels_per_unit_area_cls = ...
    min_parcels_per_facet: min_parcels_per_facet_cls = ...
    command_names = ...

    def do_initialization_now(self, ):
        """
        Apply All settings and initialize film on selected wall(s) Now?.
        """

