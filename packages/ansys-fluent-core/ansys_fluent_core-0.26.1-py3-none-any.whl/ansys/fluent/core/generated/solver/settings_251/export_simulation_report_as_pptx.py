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

from .report_name import report_name as report_name_cls
from .file_name_2 import file_name as file_name_cls

class export_simulation_report_as_pptx(Command):
    """
    Export the provided simulation report as a PPT file.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "export-simulation-report-as-pptx"

    argument_names = \
        ['report_name', 'file_name']

    _child_classes = dict(
        report_name=report_name_cls,
        file_name=file_name_cls,
    )

