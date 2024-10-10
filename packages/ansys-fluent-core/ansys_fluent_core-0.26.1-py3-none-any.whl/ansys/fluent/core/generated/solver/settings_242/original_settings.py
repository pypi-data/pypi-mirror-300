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

from .active import active as active_cls
from .name_6 import name as name_cls
from .python_cmd import python_cmd as python_cmd_cls
from .command import command as command_cls
from .count import count as count_cls
from .ftselected import ftselected as ftselected_cls
from .flowtime import flowtime as flowtime_cls

class original_settings(Group):
    """
    'original_settings' child.
    """

    fluent_name = "original-settings"

    child_names = \
        ['active', 'name', 'python_cmd', 'command', 'count', 'ftselected',
         'flowtime']

    _child_classes = dict(
        active=active_cls,
        name=name_cls,
        python_cmd=python_cmd_cls,
        command=command_cls,
        count=count_cls,
        ftselected=ftselected_cls,
        flowtime=flowtime_cls,
    )

