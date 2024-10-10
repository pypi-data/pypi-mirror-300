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

from .write_data_1 import write_data as write_data_cls
from .capture_simulation_report_data import capture_simulation_report_data as capture_simulation_report_data_cls

class create_1(CommandWithPositionalArgs):
    """
    Add new Design Point.
    
    Parameters
    ----------
        write_data : bool
            'write_data' child.
        capture_simulation_report_data : bool
            'capture_simulation_report_data' child.
    
    """

    fluent_name = "create"

    argument_names = \
        ['write_data', 'capture_simulation_report_data']

    _child_classes = dict(
        write_data=write_data_cls,
        capture_simulation_report_data=capture_simulation_report_data_cls,
    )

