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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .create_1_1 import create_1 as create_1_cls
from .duplicate_1 import duplicate as duplicate_cls
from .load_case_data import load_case_data as load_case_data_cls
from .set_as_current_1 import set_as_current as set_as_current_cls
from .delete_design_points import delete_design_points as delete_design_points_cls
from .save_journals import save_journals as save_journals_cls
from .clear_generated_data import clear_generated_data as clear_generated_data_cls
from .update_current import update_current as update_current_cls
from .update_all import update_all as update_all_cls
from .update_selected import update_selected as update_selected_cls
from .design_points_child import design_points_child


class design_points(NamedObject[design_points_child], CreatableNamedObjectMixinOld[design_points_child]):
    """
    'design_points' child.
    """

    fluent_name = "design-points"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'create_1', 'duplicate', 'load_case_data', 'set_as_current',
         'delete_design_points', 'save_journals', 'clear_generated_data',
         'update_current', 'update_all', 'update_selected']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        create_1=create_1_cls,
        duplicate=duplicate_cls,
        load_case_data=load_case_data_cls,
        set_as_current=set_as_current_cls,
        delete_design_points=delete_design_points_cls,
        save_journals=save_journals_cls,
        clear_generated_data=clear_generated_data_cls,
        update_current=update_current_cls,
        update_all=update_all_cls,
        update_selected=update_selected_cls,
    )

    child_object_type: design_points_child = design_points_child
    """
    child_object_type of design_points.
    """
