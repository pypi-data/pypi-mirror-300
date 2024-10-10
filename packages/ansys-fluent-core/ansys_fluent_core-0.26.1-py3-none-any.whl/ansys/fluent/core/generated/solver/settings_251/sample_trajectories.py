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

from .output_udf import output_udf as output_udf_cls
from .sort_sample_files import sort_sample_files as sort_sample_files_cls
from .compute_9 import compute as compute_cls
from .start_file_write import start_file_write as start_file_write_cls
from .stop_file_write import stop_file_write as stop_file_write_cls

class sample_trajectories(Group):
    """
    'sample_trajectories' child.
    """

    fluent_name = "sample-trajectories"

    child_names = \
        ['output_udf', 'sort_sample_files']

    command_names = \
        ['compute', 'start_file_write', 'stop_file_write']

    _child_classes = dict(
        output_udf=output_udf_cls,
        sort_sample_files=sort_sample_files_cls,
        compute=compute_cls,
        start_file_write=start_file_write_cls,
        stop_file_write=stop_file_write_cls,
    )

    _child_aliases = dict(
        user_defined_functions="output_udf",
    )

