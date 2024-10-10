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

from .update_interval import update_interval as update_interval_cls
from .circumferential_averaged_profile_enhanced_bands_check import circumferential_averaged_profile_enhanced_bands_check as circumferential_averaged_profile_enhanced_bands_check_cls
from .display_profile_point_cloud_data import display_profile_point_cloud_data as display_profile_point_cloud_data_cls
from .display_profile_surface import display_profile_surface as display_profile_surface_cls
from .set_preference_profile_point_cloud_data import set_preference_profile_point_cloud_data as set_preference_profile_point_cloud_data_cls
from .overlay_profile_point_cloud_data import overlay_profile_point_cloud_data as overlay_profile_point_cloud_data_cls
from .overlay_profile_surface import overlay_profile_surface as overlay_profile_surface_cls
from .list_profiles import list_profiles as list_profiles_cls
from .list_profile_parameters import list_profile_parameters as list_profile_parameters_cls
from .list_profile_parameters_with_value import list_profile_parameters_with_value as list_profile_parameters_with_value_cls
from .list_profile_fields import list_profile_fields as list_profile_fields_cls
from .delete_4 import delete as delete_cls
from .delete_all_1 import delete_all as delete_all_cls
from .query_list_profiles import query_list_profiles as query_list_profiles_cls
from .query_list_profile_fields import query_list_profile_fields as query_list_profile_fields_cls
from .query_list_profile_parameters import query_list_profile_parameters as query_list_profile_parameters_cls
from .query_list_profile_parameters_with_value import query_list_profile_parameters_with_value as query_list_profile_parameters_with_value_cls

class profiles(Group):
    """
    Profile display menu.
    """

    fluent_name = "profiles"

    child_names = \
        ['update_interval',
         'circumferential_averaged_profile_enhanced_bands_check']

    command_names = \
        ['display_profile_point_cloud_data', 'display_profile_surface',
         'set_preference_profile_point_cloud_data',
         'overlay_profile_point_cloud_data', 'overlay_profile_surface',
         'list_profiles', 'list_profile_parameters',
         'list_profile_parameters_with_value', 'list_profile_fields',
         'delete', 'delete_all']

    query_names = \
        ['query_list_profiles', 'query_list_profile_fields',
         'query_list_profile_parameters',
         'query_list_profile_parameters_with_value']

    _child_classes = dict(
        update_interval=update_interval_cls,
        circumferential_averaged_profile_enhanced_bands_check=circumferential_averaged_profile_enhanced_bands_check_cls,
        display_profile_point_cloud_data=display_profile_point_cloud_data_cls,
        display_profile_surface=display_profile_surface_cls,
        set_preference_profile_point_cloud_data=set_preference_profile_point_cloud_data_cls,
        overlay_profile_point_cloud_data=overlay_profile_point_cloud_data_cls,
        overlay_profile_surface=overlay_profile_surface_cls,
        list_profiles=list_profiles_cls,
        list_profile_parameters=list_profile_parameters_cls,
        list_profile_parameters_with_value=list_profile_parameters_with_value_cls,
        list_profile_fields=list_profile_fields_cls,
        delete=delete_cls,
        delete_all=delete_all_cls,
        query_list_profiles=query_list_profiles_cls,
        query_list_profile_fields=query_list_profile_fields_cls,
        query_list_profile_parameters=query_list_profile_parameters_cls,
        query_list_profile_parameters_with_value=query_list_profile_parameters_with_value_cls,
    )

