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

from .report_type import report_type as report_type_cls
from .surface_id import surface_id as surface_id_cls
from .add_custome_vector import add_custome_vector as add_custome_vector_cls
from .cust_vec_name import cust_vec_name as cust_vec_name_cls
from .domain_cx import domain_cx as domain_cx_cls
from .cell_cx import cell_cx as cell_cx_cls
from .domain_cy import domain_cy as domain_cy_cls
from .cell_cy import cell_cy as cell_cy_cls
from .domain_cz import domain_cz as domain_cz_cls
from .cell_cz import cell_cz as cell_cz_cls
from .cust_vec_func import cust_vec_func as cust_vec_func_cls
from .domain_report import domain_report as domain_report_cls
from .cell_report import cell_report as cell_report_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls

class surface_integrals(Command):
    """
    'surface_integrals' command.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        surface_id : List
            'surface_id' child.
        add_custome_vector : bool
            'add_custome_vector' child.
        cust_vec_name : str
            'cust_vec_name' child.
        domain_cx : str
            'domain_cx' child.
        cell_cx : str
            'cell_cx' child.
        domain_cy : str
            'domain_cy' child.
        cell_cy : str
            'cell_cy' child.
        domain_cz : str
            'domain_cz' child.
        cell_cz : str
            'cell_cz' child.
        cust_vec_func : str
            'cust_vec_func' child.
        domain_report : str
            'domain_report' child.
        cell_report : str
            'cell_report' child.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "surface-integrals"

    argument_names = \
        ['report_type', 'surface_id', 'add_custome_vector', 'cust_vec_name',
         'domain_cx', 'cell_cx', 'domain_cy', 'cell_cy', 'domain_cz',
         'cell_cz', 'cust_vec_func', 'domain_report', 'cell_report',
         'current_domain', 'write_to_file', 'file_name', 'append_data',
         'overwrite']

    _child_classes = dict(
        report_type=report_type_cls,
        surface_id=surface_id_cls,
        add_custome_vector=add_custome_vector_cls,
        cust_vec_name=cust_vec_name_cls,
        domain_cx=domain_cx_cls,
        cell_cx=cell_cx_cls,
        domain_cy=domain_cy_cls,
        cell_cy=cell_cy_cls,
        domain_cz=domain_cz_cls,
        cell_cz=cell_cz_cls,
        cust_vec_func=cust_vec_func_cls,
        domain_report=domain_report_cls,
        cell_report=cell_report_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
        overwrite=overwrite_cls,
    )

    return_type = "<object object at 0x7ff9d083ce00>"
