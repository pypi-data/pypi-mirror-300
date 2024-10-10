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

from .option import option as option_cls
from .all_2 import all as all_cls
from .feature import feature as feature_cls
from .outline import outline as outline_cls

class edge_type(Group):
    """
    'edge_type' child.
    """

    fluent_name = "edge-type"

    child_names = \
        ['option', 'all', 'feature', 'outline']

    _child_classes = dict(
        option=option_cls,
        all=all_cls,
        feature=feature_cls,
        outline=outline_cls,
    )

    return_type = "<object object at 0x7fe5b8f45620>"
