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

from .dolly import dolly as dolly_cls
from .field_1 import field as field_cls
from .orbit import orbit as orbit_cls
from .pan import pan as pan_cls
from .position_1 import position as position_cls
from .projection import projection as projection_cls
from .roll import roll as roll_cls
from .target_1 import target as target_cls
from .up_vector import up_vector as up_vector_cls
from .zoom import zoom as zoom_cls

class camera(Group):
    fluent_name = ...
    command_names = ...

    def dolly(self, right: float | str, up: float | str, in_: float | str):
        """
        Adjust the camera position and target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
            in_ : real
                'in' child.
        
        """

    def field(self, width: float | str, height: float | str):
        """
        Set the field of view (width and height).
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        
        """

    def orbit(self, right: float | str, up: float | str):
        """
        Adjust the camera position without modifying the target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        
        """

    def pan(self, right: float | str, up: float | str):
        """
        Adjust the camera position without modifying the position.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        
        """

    def position(self, xyz: List[float | str]):
        """
        Set the camera position.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        
        """

    def projection(self, type: str):
        """
        Set the camera projection.
        
        Parameters
        ----------
            type : str
                'type' child.
        
        """

    def roll(self, counter_clockwise: float | str):
        """
        Adjust the camera up-vector.
        
        Parameters
        ----------
            counter_clockwise : real
                'counter_clockwise' child.
        
        """

    def target(self, xyz: List[float | str]):
        """
        Set the point to be the center of the camera view.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        
        """

    def up_vector(self, xyz: List[float | str]):
        """
        Set the camera up-vector.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        
        """

    def zoom(self, factor: float | str):
        """
        Adjust the camera field of view.
        
        Parameters
        ----------
            factor : real
                'factor' child.
        
        """

    return_type = ...
