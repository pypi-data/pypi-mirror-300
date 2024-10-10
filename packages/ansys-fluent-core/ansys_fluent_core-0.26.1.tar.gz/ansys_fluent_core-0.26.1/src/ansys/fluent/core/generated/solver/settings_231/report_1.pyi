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

from .simulation_reports import simulation_reports as simulation_reports_cls
from .discrete_phase_1 import discrete_phase as discrete_phase_cls
from .fluxes import fluxes as fluxes_cls
from .flow import flow as flow_cls
from .modified_setting_options import modified_setting_options as modified_setting_options_cls
from .population_balance import population_balance as population_balance_cls
from .heat_exchange import heat_exchange as heat_exchange_cls
from .system import system as system_cls
from .print_write_histogram import print_write_histogram as print_write_histogram_cls
from .aero_optical_distortions import aero_optical_distortions as aero_optical_distortions_cls
from .forces import forces as forces_cls
from .mphase_summary import mphase_summary as mphase_summary_cls
from .particle_summary import particle_summary as particle_summary_cls
from .path_line_summary import path_line_summary as path_line_summary_cls
from .projected_surface_area import projected_surface_area as projected_surface_area_cls
from .summary_1 import summary as summary_cls
from .surface_integrals import surface_integrals as surface_integrals_cls
from .volume_integrals import volume_integrals as volume_integrals_cls

class report(Group):
    fluent_name = ...
    child_names = ...
    simulation_reports: simulation_reports_cls = ...
    discrete_phase: discrete_phase_cls = ...
    fluxes: fluxes_cls = ...
    flow: flow_cls = ...
    modified_setting_options: modified_setting_options_cls = ...
    population_balance: population_balance_cls = ...
    heat_exchange: heat_exchange_cls = ...
    system: system_cls = ...
    print_write_histogram: print_write_histogram_cls = ...
    command_names = ...

    def aero_optical_distortions(self, ):
        """
        Optics report menu.
        """

    def forces(self, options: str, domain_val: str, all_wall_zones: bool, wall_thread_list: List[str], direction_vector: Tuple[float | str, float | str, float | str, momentum_center: Tuple[float | str, float | str, float | str, momentum_axis: Tuple[float | str, float | str, float | str, pressure_coordinate: str, coord_val: float | str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        'forces' command.
        
        Parameters
        ----------
            options : str
                'options' child.
            domain_val : str
                'domain_val' child.
            all_wall_zones : bool
                Select all wall zones available.
            wall_thread_list : List
                'wall_thread_list' child.
            direction_vector : Tuple
                'direction_vector' child.
            momentum_center : Tuple
                'momentum_center' child.
            momentum_axis : Tuple
                'momentum_axis' child.
            pressure_coordinate : str
                'pressure_coordinate' child.
            coord_val : real
                'coord_val' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def mphase_summary(self, verbosity_option: str):
        """
        Multiphase Summary and Recommendations.
        
        Parameters
        ----------
            verbosity_option : str
                'verbosity_option' child.
        
        """

    def particle_summary(self, injection_names: List[str]):
        """
        Print summary report for all current particles.
        
        Parameters
        ----------
            injection_names : List
                'injection_names' child.
        
        """

    def path_line_summary(self, ):
        """
        Print path-line-summary report.
        """

    def projected_surface_area(self, surface_id_val: List[int], min_feature_size: float | str, proj_plane_norm_comp: Tuple[float | str, float | str, float | str):
        """
        Print total area of the projection of a group of surfaces to a plane.
        
        Parameters
        ----------
            surface_id_val : List
                'surface_id_val' child.
            min_feature_size : real
                'min_feature_size' child.
            proj_plane_norm_comp : Tuple
                'proj_plane_norm_comp' child.
        
        """

    def summary(self, write_to_file: bool, file_name: str, overwrite: bool):
        """
        Print report summary.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def surface_integrals(self, report_type: str, surface_id: List[str], add_custome_vector: bool, cust_vec_name: str, domain_cx: str, cell_cx: str, domain_cy: str, cell_cy: str, domain_cz: str, cell_cz: str, cust_vec_func: str, domain_report: str, cell_report: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        'surface_integrals' command.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            surface_id : List
                'surface_id' child.
            add_custome_vector : bool
                'add_custome_vector' child.
            cust_vec_name : str
                'cust_vec_name' child.
            domain_cx : str
                'domain_cx' child.
            cell_cx : str
                'cell_cx' child.
            domain_cy : str
                'domain_cy' child.
            cell_cy : str
                'cell_cy' child.
            domain_cz : str
                'domain_cz' child.
            cell_cz : str
                'cell_cz' child.
            cust_vec_func : str
                'cust_vec_func' child.
            domain_report : str
                'domain_report' child.
            cell_report : str
                'cell_report' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def volume_integrals(self, report_type: str, thread_id_list: List[str], domain: str, cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        'volume_integrals' command.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            thread_id_list : List
                'thread_id_list' child.
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        
        """

    return_type = ...
