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

from .file_name_1 import file_name as file_name_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class fieldview_data(Command):
    """
    Write Fieldview case and data files.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        cell_func_domain_export : List
            Select the list of quantities to export.
    
    """

    fluent_name = "fieldview-data"

    argument_names = \
        ['file_name', 'cell_func_domain_export']

    _child_classes = dict(
        file_name=file_name_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

