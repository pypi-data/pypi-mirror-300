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

from .picture_options import picture_options as picture_options_cls
from .camera import camera as camera_cls
from .display_states import display_states as display_states_cls
from .save_picture import save_picture as save_picture_cls
from .auto_scale_1 import auto_scale as auto_scale_cls
from .reset_to_default_view import reset_to_default_view as reset_to_default_view_cls
from .delete_view import delete_view as delete_view_cls
from .last_view import last_view as last_view_cls
from .next_view import next_view as next_view_cls
from .restore_view import restore_view as restore_view_cls
from .read_views import read_views as read_views_cls
from .save_view import save_view as save_view_cls
from .write_views import write_views as write_views_cls

class views(Group):
    fluent_name = ...
    child_names = ...
    picture_options: picture_options_cls = ...
    camera: camera_cls = ...
    display_states: display_states_cls = ...
    command_names = ...

    def save_picture(self, file_name: str):
        """
        'save_picture' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def auto_scale(self, ):
        """
        'auto_scale' command.
        """

    def reset_to_default_view(self, ):
        """
        Reset view to front and center.
        """

    def delete_view(self, view_name: str):
        """
        Remove a view from the list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def last_view(self, ):
        """
        Return to the camera position before the last manipulation.
        """

    def next_view(self, ):
        """
        Return to the camera position after the current position in the stack.
        """

    def restore_view(self, view_name: str):
        """
        Use a saved view.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def read_views(self, filename: str):
        """
        Read views from a view file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def save_view(self, view_name: str):
        """
        Save the current view to the view list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        
        """

    def write_views(self, file_name: str, view_list: List[str]):
        """
        Write selected views to a view file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            view_list : List
                'view_list' child.
        
        """

    return_type = ...
