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

    def solution_controls(self, mf: int, urf: float | str):
        """
        Specification of mapped frequency and under-relaxation factor for mapped interfaces.
        
        Parameters
        ----------
            mf : int
                'mf' child.
            urf : real
                'urf' child.
        
        """

    def tolerance(self, use_local_edge_length_factor: bool, gtol_length_factor: float | str, gtol_absolute_value: float | str, update: bool):
        """
        Specification of mapped interface tolerance.
        
        Parameters
        ----------
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                'gtol_length_factor' child.
            gtol_absolute_value : real
                'gtol_absolute_value' child.
            update : bool
                Update mapped interface with new tolerance.
        
        """

    def convert_to_mapped_interface(self, all: bool, auto: bool, use_local_edge_length_factor: bool, gtol_length_factor: float | str, gtol_absolute_value: float | str):
        """
        Convert non-conformal mesh interface to mapped mesh interfaces.
        
        Parameters
        ----------
            all : bool
                Convert all mesh interfaces to mapped mesh interfaces.
            auto : bool
                Convert poorly matching mesh interfaces to mapped mesh interfaces.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            gtol_length_factor : real
                'gtol_length_factor' child.
            gtol_absolute_value : real
                'gtol_absolute_value' child.
        
        """

    return_type = ...
