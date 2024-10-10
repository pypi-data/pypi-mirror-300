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

from .solution_controls import solution_controls as solution_controls_cls
from .tolerance_1 import tolerance as tolerance_cls
from .convert_to_mapped_interface import convert_to_mapped_interface as convert_to_mapped_interface_cls

class mapped_interface_options(Group):
    fluent_name = ...
    command_names = ...

    def solution_controls(self, mapping_frequency: int, under_relaxation_factor: float | str):
        """
        Specification of mapped frequency and under-relaxation factor for mapped interfaces.
        
        Parameters
        ----------
            mapping_frequency : int
                Mapping Frequency.
            under_relaxation_factor : real
                Under-Relaxation Factor.
        
        """

    def tolerance(self, use_local_edge_length_factor: bool, gtol_length_factor: float | str, gtol_absolute_value: float | str, update: bool):
        """
        Specification of mapped interface tolerance.
        
        Parameters
        ----------
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                Tolerance.
            gtol_absolute_value : real
                Tolerance.
            update : bool
                Update mapped interface with new tolerance.
        
        """

    def convert_to_mapped_interface(self, convert_all: bool, convert_poorly_matching: bool, use_local_edge_length_factor: bool, gtol_length_factor: float | str, gtol_absolute_value: float | str):
        """
        Convert non-conformal mesh interface to mapped mesh interfaces.
        
        Parameters
        ----------
            convert_all : bool
                Convert all mesh interfaces to mapped mesh interfaces.
            convert_poorly_matching : bool
                Convert poorly matching mesh interfaces to mapped mesh interfaces.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                Tolerance.
            gtol_absolute_value : real
                Tolerance.
        
        """

