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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .copy import copy as copy_cls
from .beams_child import beams_child


class beams(NamedObject[beams_child], CreatableNamedObjectMixinOld[beams_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : str
                'to' child.
        
        """

    def copy(self, orig_beam_name: str, beam_name: str, ap_face_zone: str, beam_length: float | str, ray_npoints: int, x_beam_vector: float | str, y_beam_vector: float | str, z_beam_vector: float | str):
        """
        Copy optical beam grid.
        
        Parameters
        ----------
            orig_beam_name : str
                Choose the name for the optical beam to be copied.
            beam_name : str
                Set a unique name for each optical beam.
            ap_face_zone : str
                Set the wall face zones to specify the optical aperture surface.
            beam_length : real
                Set the length of optical beam propagation.
            ray_npoints : int
                Set the number of grid point in each ray of the optical beam.
            x_beam_vector : real
                Set the x-component of the beam propagation vector.
            y_beam_vector : real
                Set the y-component of the beam propagation vector.
            z_beam_vector : real
                Set the z-component of the beam propagation vector.
        
        """

    child_object_type: beams_child = ...
    return_type = ...
