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

from .output_udf import output_udf as output_udf_cls
from .sort_sample_files import sort_sample_files as sort_sample_files_cls
from .compute_9 import compute as compute_cls
from .start_file_write import start_file_write as start_file_write_cls
from .stop_file_write import stop_file_write as stop_file_write_cls

class sample_trajectories(Group):
    fluent_name = ...
    child_names = ...
    output_udf: output_udf_cls = ...
    sort_sample_files: sort_sample_files_cls = ...
    command_names = ...

    def compute(self, injections: List[str], boundaries: List[str], lines: List[str], planes: List[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'compute' command.
        
        Parameters
        ----------
            injections : List
                'injections' child.
            boundaries : List
                'boundaries' child.
            lines : List
                Select surface.
            planes : List
                Select surface.
            op_udf : str
                'op_udf' child.
            append_sample : bool
                'append_sample' child.
            accumulate_rates : bool
                'accumulate_rates' child.
        
        """

    def start_file_write(self, injections: List[str], boundaries: List[str], lines: List[str], planes: List[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'start_file_write' command.
        
        Parameters
        ----------
            injections : List
                'injections' child.
            boundaries : List
                'boundaries' child.
            lines : List
                Select surface.
            planes : List
                Select surface.
            op_udf : str
                'op_udf' child.
            append_sample : bool
                'append_sample' child.
            accumulate_rates : bool
                'accumulate_rates' child.
        
        """

    def stop_file_write(self, ):
        """
        'stop_file_write' command.
        """

