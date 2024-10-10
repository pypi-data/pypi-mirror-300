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

from .anode_tab import anode_tab as anode_tab_cls
from .cathode_tab import cathode_tab as cathode_tab_cls

class electrical_tab(Group):
    """
    Set up external electrical tabs.
    """

    fluent_name = "electrical-tab"

    child_names = \
        ['anode_tab', 'cathode_tab']

    _child_classes = dict(
        anode_tab=anode_tab_cls,
        cathode_tab=cathode_tab_cls,
    )

