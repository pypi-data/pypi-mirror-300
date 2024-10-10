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

from .files_1 import files as files_cls

class remove(Command):
    """
    Remove a selection of imported training data files.
    
    Parameters
    ----------
        files : List
            List of training data files to remove.
    
    """

    fluent_name = "remove"

    argument_names = \
        ['files']

    _child_classes = dict(
        files=files_cls,
    )

