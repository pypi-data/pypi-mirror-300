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

from .option_25 import option as option_cls
from .automatic import automatic as automatic_cls
from .manual import manual as manual_cls

class coloring(Group):
    """
    Enter the coloring options menu.
    """

    fluent_name = "coloring"

    child_names = \
        ['option', 'automatic', 'manual']

    _child_classes = dict(
        option=option_cls,
        automatic=automatic_cls,
        manual=manual_cls,
    )

