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

from .invalidate_case import invalidate_case as invalidate_case_cls
from .delete_all_compute_nodes import delete_all_compute_nodes as delete_all_compute_nodes_cls

class kill_all_nodes(Command):
    """
    Delete all compute nodes from virtual machine.
    
    Parameters
    ----------
        invalidate_case : bool
            'invalidate_case' child.
        delete_all_compute_nodes : bool
            'delete_all_compute_nodes' child.
    
    """

    fluent_name = "kill-all-nodes"

    argument_names = \
        ['invalidate_case', 'delete_all_compute_nodes']

    _child_classes = dict(
        invalidate_case=invalidate_case_cls,
        delete_all_compute_nodes=delete_all_compute_nodes_cls,
    )

    return_type = "<object object at 0x7fe5b8d3c6d0>"
