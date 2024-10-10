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

from .options_4 import options as options_cls
from .parameters import parameters as parameters_cls
from .anode import anode as anode_cls
from .electrolyte import electrolyte as electrolyte_cls
from .cathode import cathode as cathode_cls
from .electrical_tab import electrical_tab as electrical_tab_cls
from .advanced import advanced as advanced_cls

class electrolysis(Group):
    """
    'electrolysis' child.
    """

    fluent_name = "electrolysis"

    child_names = \
        ['options', 'parameters', 'anode', 'electrolyte', 'cathode',
         'electrical_tab', 'advanced']

    _child_classes = dict(
        options=options_cls,
        parameters=parameters_cls,
        anode=anode_cls,
        electrolyte=electrolyte_cls,
        cathode=cathode_cls,
        electrical_tab=electrical_tab_cls,
        advanced=advanced_cls,
    )

    return_type = "<object object at 0x7fd94d0e7700>"
