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

from .name_6 import name as name_cls
from .file_name_2_1 import file_name_2 as file_name_2_cls
from .frequency_of import frequency_of as frequency_of_cls
from .frequency_1 import frequency as frequency_cls
from .flow_frequency import flow_frequency as flow_frequency_cls
from .itr_index import itr_index as itr_index_cls
from .run_index import run_index as run_index_cls
from .report_defs_1 import report_defs as report_defs_cls
from .print_3 import print as print_cls
from .active import active as active_cls
from .write_instantaneous_values import write_instantaneous_values as write_instantaneous_values_cls

class report_files_child(Group):
    """
    'child_object_type' of report_files.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'file_name', 'frequency_of', 'frequency', 'flow_frequency',
         'itr_index', 'run_index', 'report_defs', 'print', 'active',
         'write_instantaneous_values']

    _child_classes = dict(
        name=name_cls,
        file_name=file_name_2_cls,
        frequency_of=frequency_of_cls,
        frequency=frequency_cls,
        flow_frequency=flow_frequency_cls,
        itr_index=itr_index_cls,
        run_index=run_index_cls,
        report_defs=report_defs_cls,
        print=print_cls,
        active=active_cls,
        write_instantaneous_values=write_instantaneous_values_cls,
    )

