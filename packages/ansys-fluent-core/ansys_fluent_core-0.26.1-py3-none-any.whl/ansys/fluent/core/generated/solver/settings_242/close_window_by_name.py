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

from .window_name import window_name as window_name_cls

class close_window_by_name(Command):
    """
    Close a reserved graphics window by its name.
    
    Parameters
    ----------
        window_name : str
            'window_name' child.
    
    """

    fluent_name = "close-window-by-name"

    argument_names = \
        ['window_name']

    _child_classes = dict(
        window_name=window_name_cls,
    )

