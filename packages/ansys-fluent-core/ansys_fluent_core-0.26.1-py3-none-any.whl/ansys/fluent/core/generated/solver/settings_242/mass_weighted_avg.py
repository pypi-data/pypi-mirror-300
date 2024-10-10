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

from .surface_names_2 import surface_names as surface_names_cls
from .geometry_names import geometry_names as geometry_names_cls
from .cust_vec_func import cust_vec_func as cust_vec_func_cls
from .report_of import report_of as report_of_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class mass_weighted_avg(Command):
    """
    Print mass-average of scalar over surfaces.
    
    Parameters
    ----------
        surface_names : List
            Select surface.
        geometry_names : List
            Select UTL Geometry.
        cust_vec_func : str
            Specify the custom vectors.
        report_of : str
            Specify Field.
        current_domain : str
            Select the domain.
        write_to_file : bool
            Choose whether or not to write to a file.
        file_name : str
            Enter the name you want the file saved with.
        append_data : bool
            Choose whether or not to append data to existing file.
    
    """

    fluent_name = "mass-weighted-avg"

    argument_names = \
        ['surface_names', 'geometry_names', 'cust_vec_func', 'report_of',
         'current_domain', 'write_to_file', 'file_name', 'append_data']

    _child_classes = dict(
        surface_names=surface_names_cls,
        geometry_names=geometry_names_cls,
        cust_vec_func=cust_vec_func_cls,
        report_of=report_of_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

