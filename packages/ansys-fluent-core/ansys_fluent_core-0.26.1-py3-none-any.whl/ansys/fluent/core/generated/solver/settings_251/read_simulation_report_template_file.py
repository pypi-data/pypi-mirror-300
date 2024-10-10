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

from .file_name_1_3 import file_name_1 as file_name_1_cls

class read_simulation_report_template_file(Command):
    """
    Read a JSON template file with existing Simulation Report settings.
    
    Parameters
    ----------
        file_name_1 : str
            'file_name' child.
    
    """

    fluent_name = "read-simulation-report-template-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

