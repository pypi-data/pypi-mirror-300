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
    fluent_name = ...
    child_names = ...
    update_interval: update_interval_cls = ...
    circumferential_averaged_profile_enhanced_bands_check: circumferential_averaged_profile_enhanced_bands_check_cls = ...
    command_names = ...

    def display_profile_point_cloud_data(self, profile_name: str, field_contour: bool, field_variable: str):
        """
        Display Profile Point cloud data Command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
            field_contour : bool
                Field contour?.
            field_variable : str
                Field variable.
        
        """

    def display_profile_surface(self, profile_name: str, field_contour: bool, field_variable: str):
        """
        Display Profile Surface/field rendering command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
            field_contour : bool
                Field contour?.
            field_variable : str
                Field variable.
        
        """

    def set_preference_profile_point_cloud_data(self, profile_point_marker: str, profile_point_marker_size: float | str, profile_point_marker_color: str):
        """
        Profile Point attributes command.
        
        Parameters
        ----------
            profile_point_marker : str
                Profile point marker.
            profile_point_marker_size : real
                Profile point marker size.
            profile_point_marker_color : str
                Profile point marker color.
        
        """

    def overlay_profile_point_cloud_data(self, overlay: bool, profile_name: str, graphics_object: str, display_contour: bool, field_variable: str):
        """
        Overlay Display Profile Point cloud data Command.
        
        Parameters
        ----------
            overlay : bool
                Overlay profile point cloud data.
            profile_name : str
                Profile name.
            graphics_object : str
                Graphics Object.
            display_contour : bool
                Enable/Disable Profile Field Contour.
            field_variable : str
                Field variable.
        
        """

    def overlay_profile_surface(self, overlay: bool, profile_name: str, graphics_object: str, field_contour: bool, filed_variable: str):
        """
        Overlay Display Profile Surface Command.
        
        Parameters
        ----------
            overlay : bool
                Overlay profile surface.
            profile_name : str
                Profile name.
            graphics_object : str
                Graphics Object.
            field_contour : bool
                Field contour?.
            filed_variable : str
                Field variable.
        
        """

    def list_profiles(self, ):
        """
        List-profiles-command.
        """

    def list_profile_parameters(self, profile_name: str):
        """
        List-profile-parameters-command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def list_profile_parameters_with_value(self, profile_name: str):
        """
        List-profile-parameters-with-value-command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def list_profile_fields(self, profile_name: str):
        """
        List-profile-fields-command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def delete(self, profile_name: str):
        """
        Delete-profile-command.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def delete_all(self, ):
        """
        Delete-all-command.
        """

    query_names = ...

    def query_list_profiles(self, ):
        """
        List-profiles-command.
        """

    def query_list_profile_fields(self, profile_name: str):
        """
        Query list-profile-fields.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def query_list_profile_parameters(self, profile_name: str):
        """
        Query-list-profile-parameters-class.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

    def query_list_profile_parameters_with_value(self, profile_name: str):
        """
        Query-list-profile-parameters-with-value-class.
        
        Parameters
        ----------
            profile_name : str
                Profile name.
        
        """

