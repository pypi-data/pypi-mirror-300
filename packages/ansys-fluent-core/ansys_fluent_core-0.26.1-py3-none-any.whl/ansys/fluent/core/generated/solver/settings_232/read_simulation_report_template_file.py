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

from .file_name_path_1 import file_name_path as file_name_path_cls

class read_simulation_report_template_file(Command):
    """
    Read a JSON template file with existing Simulation Report settings.
    
    Parameters
    ----------
        file_name_path : str
            'file_name_path' child.
    
    """

    fluent_name = "read-simulation-report-template-file"

    argument_names = \
        ['file_name_path']

    _child_classes = dict(
        file_name_path=file_name_path_cls,
    )

    return_type = "<object object at 0x7fe5b8e2e300>"
