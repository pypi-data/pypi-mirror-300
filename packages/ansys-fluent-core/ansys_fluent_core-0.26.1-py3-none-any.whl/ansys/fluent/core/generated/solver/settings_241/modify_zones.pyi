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

from .deactivate_cell_zone import deactivate_cell_zone as deactivate_cell_zone_cls
from .delete_cell_zone import delete_cell_zone as delete_cell_zone_cls
from .copy_move_cell_zone import copy_move_cell_zone as copy_move_cell_zone_cls
from .list_zones import list_zones as list_zones_cls
from .extrude_face_zone_delta import extrude_face_zone_delta as extrude_face_zone_delta_cls
from .extrude_face_zone_para import extrude_face_zone_para as extrude_face_zone_para_cls
from .fuse_face_zones import fuse_face_zones as fuse_face_zones_cls
from .scale_zone import scale_zone as scale_zone_cls
from .rotate_zone import rotate_zone as rotate_zone_cls
from .translate_zone import translate_zone as translate_zone_cls
from .merge_zones import merge_zones as merge_zones_cls
from .replace_zone import replace_zone as replace_zone_cls
from .append_mesh import append_mesh as append_mesh_cls
from .append_mesh_data import append_mesh_data as append_mesh_data_cls
from .sep_cell_zone_mark import sep_cell_zone_mark as sep_cell_zone_mark_cls
from .sep_cell_zone_region import sep_cell_zone_region as sep_cell_zone_region_cls
from .sep_face_zone_angle import sep_face_zone_angle as sep_face_zone_angle_cls
from .sep_face_zone_face import sep_face_zone_face as sep_face_zone_face_cls
from .sep_face_zone_mark import sep_face_zone_mark as sep_face_zone_mark_cls
from .sep_face_zone_region import sep_face_zone_region as sep_face_zone_region_cls
from .zone_name_2 import zone_name as zone_name_cls
from .change_zone_state import change_zone_state as change_zone_state_cls
from .make_periodic import make_periodic as make_periodic_cls
from .create_periodic_interface import create_periodic_interface as create_periodic_interface_cls
from .slit_periodic_1 import slit_periodic as slit_periodic_cls
from .zone_type import zone_type as zone_type_cls

class modify_zones(Group):
    fluent_name = ...
    command_names = ...

    def deactivate_cell_zone(self, cell_deactivate_list: List[str]):
        """
        Deactivate cell thread.
        
        Parameters
        ----------
            cell_deactivate_list : List
                Deactivate a cell zone.
        
        """

    def delete_cell_zone(self, cell_zones: List[str]):
        """
        Delete a cell thread.
        
        Parameters
        ----------
            cell_zones : List
                Delete a cell zone.
        
        """

    def copy_move_cell_zone(self, cell_zone_name: str, translate: bool, rotation_angle: float | str, offset: List[float | str], axis: List[float | str]):
        """
        Copy and translate or rotate a cell zone.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a cell zone name.
            translate : bool
                Specify if copied zone should be translated (#t) or rotated (#f).
            rotation_angle : real
                'rotation_angle' child.
            offset : List
                'offset' child.
            axis : List
                'axis' child.
        
        """

    def list_zones(self, ):
        """
        List zone IDs, types, kinds, and names.
        """

    def extrude_face_zone_delta(self, face_zone: str, distance_delta: List[float | str]):
        """
        Extrude a face thread a specified distance based on a list of deltas.
        
        Parameters
        ----------
            face_zone : str
                Enter a zone name.
            distance_delta : List
                'distance_delta' child.
        
        """

    def extrude_face_zone_para(self, face_zone: str, normal_distance: float | str, parametric_coordinates: List[float | str]):
        """
        Extrude a face thread a specified distance based on a distance and a list of parametric locations between 0 and 1 (eg. 0 0.2 0.4 0.8 1.0).
        
        Parameters
        ----------
            face_zone : str
                Enter a zone name.
            normal_distance : real
                'normal_distance' child.
            parametric_coordinates : List
                'parametric_coordinates' child.
        
        """

    def fuse_face_zones(self, zone_names: List[str], zone_name: str):
        """
        Attempt to fuse zones by removing duplicate faces and nodes.
        
        Parameters
        ----------
            zone_names : List
                Merge duplicate faces and nodes of zones in list.
            zone_name : str
                'zone_name' child.
        
        """

    def scale_zone(self, zone_names: List[str], scale: List[float | str]):
        """
        Scale nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : List
                Scale specified cell zones.
            scale : List
                'scale' child.
        
        """

    def rotate_zone(self, zone_names: List[str], rotation_angle: float | str, origin: List[float | str], axis: List[float | str]):
        """
        Rotate nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : List
                Rotate specified cell zones.
            rotation_angle : real
                'rotation_angle' child.
            origin : List
                'origin' child.
            axis : List
                'axis' child.
        
        """

    def translate_zone(self, zone_names: List[str], offset: List[float | str]):
        """
        Translate nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : List
                Translate specified cell zones.
            offset : List
                'offset' child.
        
        """

    def merge_zones(self, zone_names: List[str]):
        """
        Merge zones of the same type and condition into one.
        
        Parameters
        ----------
            zone_names : List
                Enter zone name list.
        
        """

    def replace_zone(self, file_name: str, zone_1_name: str, zone_2_name: str, interpolate: bool):
        """
        Replace a cell zone.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            zone_1_name : str
                Enter a zone name.
            zone_2_name : str
                'zone_2_name' child.
            interpolate : bool
                'interpolate' child.
        
        """

    def append_mesh(self, file_name: str):
        """
        Append new mesh.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def append_mesh_data(self, file_name: str):
        """
        Append new mesh with data.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def sep_cell_zone_mark(self, cell_zone_name: str, register: str, move_faces: bool):
        """
        Separate a cell zone based on cell marking.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a zone name.
            register : str
                'register' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_cell_zone_region(self, cell_zone_name: str, move_cells: bool):
        """
        Separate a cell zone based on contiguous regions.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a zone name.
            move_cells : bool
                'move_cells' child.
        
        """

    def sep_face_zone_angle(self, face_zone_name: str, angle: float | str, move_faces: bool):
        """
        Separate a face zone based on significant angle.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            angle : real
                'angle' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_face(self, face_zone_name: str, move_faces: bool):
        """
        Separate each face in a zone into unique zone.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_mark(self, face_zone_name: str, register_name: str, move_faces: bool):
        """
        Separate a face zone based on cell marking.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            register_name : str
                'register_name' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_region(self, face_zone_name: str, move_faces: bool):
        """
        Separate a face zone based on contiguous regions.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            move_faces : bool
                'move_faces' child.
        
        """

    def zone_name(self, zone_name: str, new_name: str):
        """
        Give a zone a new name.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            new_name : str
                'new_name' child.
        
        """

    def change_zone_state(self, zone_name: str, domain: str, new_phase: int):
        """
        Change the realgas material state for a zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a fluid zone name.
            domain : str
                'domain' child.
            new_phase : int
                'new_phase' child.
        
        """

    def make_periodic(self, zone_name: str, shadow_zone_name: str, rotate_periodic: bool, create: bool, auto_translation: bool, direction: List[float | str]):
        """
        Attempt to establish conformal periodic face zone connectivity.
        
        Parameters
        ----------
            zone_name : str
                Enter id/name of zone to convert to periodic.
            shadow_zone_name : str
                Enter id/name of zone to convert to shadow.
            rotate_periodic : bool
                'rotate_periodic' child.
            create : bool
                'create' child.
            auto_translation : bool
                'auto_translation' child.
            direction : List
                'direction' child.
        
        """

    def create_periodic_interface(self, periodic_method: str, interface_name: str, zone_name: str, shadow_zone_name: str, rotate_periodic: bool, new_axis: bool, origin: List[float | str], new_direction: bool, direction: List[float | str], auto_angle: bool, rotation_angle: float | str, auto_translation: bool, translation: List[float | str], create_periodic: bool, auto_offset: bool, nonconformal_angle: float | str, nonconformal_translation: List[float | str], create_matching: bool, nonconformal_create_periodic: bool):
        """
        Create a conformal or non-conformal periodic interface.
        
        Parameters
        ----------
            periodic_method : str
                Enter method.
            interface_name : str
                Enter a name for this periodic interface.
            zone_name : str
                Enter id/name of zone to convert to periodic.
            shadow_zone_name : str
                Enter id/name of zone to convert to shadow.
            rotate_periodic : bool
                'rotate_periodic' child.
            new_axis : bool
                'new_axis' child.
            origin : List
                'origin' child.
            new_direction : bool
                'new_direction' child.
            direction : List
                'direction' child.
            auto_angle : bool
                'auto_angle' child.
            rotation_angle : real
                'rotation_angle' child.
            auto_translation : bool
                'auto_translation' child.
            translation : List
                'translation' child.
            create_periodic : bool
                'create_periodic' child.
            auto_offset : bool
                'auto_offset' child.
            nonconformal_angle : real
                'nonconformal_angle' child.
            nonconformal_translation : List
                'nonconformal_translation' child.
            create_matching : bool
                'create_matching' child.
            nonconformal_create_periodic : bool
                'nonconformal_create_periodic' child.
        
        """

    def slit_periodic(self, periodic_zone_name: str, slit_periodic: bool):
        """
        Slit a periodic zone into two symmetry zones.
        
        Parameters
        ----------
            periodic_zone_name : str
                Enter id/name of periodic zone to slit.
            slit_periodic : bool
                'slit_periodic' child.
        
        """

    def zone_type(self, zone_names: List[str], new_type: str):
        """
        Set a zone's type.
        
        Parameters
        ----------
            zone_names : List
                Enter zone id/name.
            new_type : str
                'new_type' child.
        
        """

    return_type = ...
