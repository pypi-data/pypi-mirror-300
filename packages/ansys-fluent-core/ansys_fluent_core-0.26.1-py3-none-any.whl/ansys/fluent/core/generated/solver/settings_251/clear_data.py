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

from .report_files import report_files as report_files_cls

class clear_data(Command):
    """
    Allows you to delete the report file from system.
    
    Parameters
    ----------
        report_files : List
            Specify the Report files.
    
    """

    fluent_name = "clear-data"

    argument_names = \
        ['report_files']

    _child_classes = dict(
        report_files=report_files_cls,
    )

