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

from .file_path import file_path as file_path_cls

class write_simulation_report_names_to_file(Command):
    """
    Write the list of currently generated report names to a txt file.
    
    Parameters
    ----------
        file_path : str
            'file_path' child.
    
    """

    fluent_name = "write-simulation-report-names-to-file"

    argument_names = \
        ['file_path']

    _child_classes = dict(
        file_path=file_path_cls,
    )

    return_type = "<object object at 0x7fe5b8e2e230>"
