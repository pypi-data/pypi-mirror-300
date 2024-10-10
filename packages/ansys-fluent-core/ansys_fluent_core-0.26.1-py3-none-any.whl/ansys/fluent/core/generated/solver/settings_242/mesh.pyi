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

from .adapt import adapt as adapt_cls
from .anisotropic_adaption import anisotropic_adaption as anisotropic_adaption_cls
from .check_before_solve import check_before_solve as check_before_solve_cls
from .check_verbosity import check_verbosity as check_verbosity_cls
from .enhanced_orthogonal_quality import enhanced_orthogonal_quality as enhanced_orthogonal_quality_cls
from .matching_tolerance import matching_tolerance as matching_tolerance_cls
from .modify_zones import modify_zones as modify_zones_cls
from .show_periodic_shadow_zones import show_periodic_shadow_zones as show_periodic_shadow_zones_cls
from .reorder import reorder as reorder_cls
from .repair_improve import repair_improve as repair_improve_cls
from .surface_mesh import surface_mesh as surface_mesh_cls
from .polyhedra import polyhedra as polyhedra_cls
from .wall_distance_method import wall_distance_method as wall_distance_method_cls
from .adjacency import adjacency as adjacency_cls
from .check import check as check_cls
from .memory_usage import memory_usage as memory_usage_cls
from .mesh_info import mesh_info as mesh_info_cls
from .quality import quality as quality_cls
from .rotate import rotate as rotate_cls
from .scale_1 import scale as scale_cls
from .size_info import size_info as size_info_cls
from .redistribute_boundary_layer import redistribute_boundary_layer as redistribute_boundary_layer_cls
from .swap_mesh_faces import swap_mesh_faces as swap_mesh_faces_cls
from .smooth_mesh import smooth_mesh as smooth_mesh_cls
from .replace import replace as replace_cls
from .translate_1 import translate as translate_cls

class mesh(Group):
    fluent_name = ...
    child_names = ...
    adapt: adapt_cls = ...
    anisotropic_adaption: anisotropic_adaption_cls = ...
    check_before_solve: check_before_solve_cls = ...
    check_verbosity: check_verbosity_cls = ...
    enhanced_orthogonal_quality: enhanced_orthogonal_quality_cls = ...
    matching_tolerance: matching_tolerance_cls = ...
    modify_zones: modify_zones_cls = ...
    show_periodic_shadow_zones: show_periodic_shadow_zones_cls = ...
    reorder: reorder_cls = ...
    repair_improve: repair_improve_cls = ...
    surface_mesh: surface_mesh_cls = ...
    polyhedra: polyhedra_cls = ...
    wall_distance_method: wall_distance_method_cls = ...
    command_names = ...

    def adjacency(self, ):
        """
        View and rename face zones adjacent to selected cell zones.
        """

    def check(self, ):
        """
        Perform various mesh consistency checks.
        """

    def memory_usage(self, ):
        """
        Report solver memory use.
        """

    def mesh_info(self, print_level: int):
        """
        Print zone information size.
        
        Parameters
        ----------
            print_level : int
                Print zone information size.
        
        """

    def quality(self, ):
        """
        Perform analysis of mesh quality.
        """

    def rotate(self, angle: float | str, origin: List[float | str], axis_components: List[float | str]):
        """
        Rotate the mesh.
        
        Parameters
        ----------
            angle : real
                'angle' child.
            origin : List
                'origin' child.
            axis_components : List
                'axis_components' child.
        
        """

    def scale(self, x_scale: float | str, y_scale: float | str, z_scale: float | str):
        """
        'scale' command.
        
        Parameters
        ----------
            x_scale : real
                'x_scale' child.
            y_scale : real
                'y_scale' child.
            z_scale : real
                'z_scale' child.
        
        """

    def size_info(self, ):
        """
        Print mesh size.
        """

    def redistribute_boundary_layer(self, zone_name: str, growth_rate: float | str):
        """
        Enforce growth rate in boundary layer.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            growth_rate : real
                'growth_rate' child.
        
        """

    def swap_mesh_faces(self, ):
        """
        Swap mesh faces.
        """

    def smooth_mesh(self, type_of_smoothing: str, number_of_iterations: int, relaxtion_factor: float | str, percentage_of_cells: float | str, skewness_threshold: float | str):
        """
        Smooth the mesh using quality-based, Laplace or skewness methods.
        
        Parameters
        ----------
            type_of_smoothing : str
                'type_of_smoothing' child.
            number_of_iterations : int
                'number_of_iterations' child.
            relaxtion_factor : real
                'relaxtion_factor' child.
            percentage_of_cells : real
                'percentage_of_cells' child.
            skewness_threshold : real
                'skewness_threshold' child.
        
        """

    def replace(self, file_name_1: str, zones: bool):
        """
        Replace mesh and interpolate data.
        
        Parameters
        ----------
            file_name_1 : str
                'file_name' child.
            zones : bool
                'zones' child.
        
        """

    def translate(self, offset: List[float | str]):
        """
        Translate the mesh.
        
        Parameters
        ----------
            offset : List
                'offset' child.
        
        """

