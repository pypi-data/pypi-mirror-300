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

from .project_filename import project_filename as project_filename_cls
from .load_case import load_case as load_case_cls

class open(Command):
    """
    Open project.
    
    Parameters
    ----------
        project_filename : str
            'project_filename' child.
        load_case : bool
            'load_case' child.
    
    """

    fluent_name = "open"

    argument_names = \
        ['project_filename', 'load_case']

    _child_classes = dict(
        project_filename=project_filename_cls,
        load_case=load_case_cls,
    )

    return_type = "<object object at 0x7ff9d2a0e9b0>"
