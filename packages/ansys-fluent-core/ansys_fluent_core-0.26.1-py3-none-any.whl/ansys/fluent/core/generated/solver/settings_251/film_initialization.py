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

from .enabled_41 import enabled as enabled_cls
from .film_height import film_height as film_height_cls
from .film_velocity import film_velocity as film_velocity_cls
from .film_temperature import film_temperature as film_temperature_cls
from .injection import injection as injection_cls
from .min_parcels_per_unit_area import min_parcels_per_unit_area as min_parcels_per_unit_area_cls
from .min_parcels_per_facet import min_parcels_per_facet as min_parcels_per_facet_cls
from .do_initialization_now import do_initialization_now as do_initialization_now_cls

class film_initialization(Group):
    """
    Patch an initial film, uniformly distributed on the entire wall zone, to begin the calculation with, based on specified film properties.
    """

    fluent_name = "film-initialization"

    child_names = \
        ['enabled', 'film_height', 'film_velocity', 'film_temperature',
         'injection', 'min_parcels_per_unit_area', 'min_parcels_per_facet']

    command_names = \
        ['do_initialization_now']

    _child_classes = dict(
        enabled=enabled_cls,
        film_height=film_height_cls,
        film_velocity=film_velocity_cls,
        film_temperature=film_temperature_cls,
        injection=injection_cls,
        min_parcels_per_unit_area=min_parcels_per_unit_area_cls,
        min_parcels_per_facet=min_parcels_per_facet_cls,
        do_initialization_now=do_initialization_now_cls,
    )

    _child_aliases = dict(
        dpm_do_patch_lwf_now="do_initialization_now",
        dpm_film_parcel_density="min_parcels_per_unit_area",
        dpm_initial_height="film_height",
        dpm_initial_injection="injection",
        dpm_initial_temperature="film_temperature",
        dpm_initialize_lwf="enabled",
        dpm_minimum_number_of_parcels="min_parcels_per_facet",
    )

