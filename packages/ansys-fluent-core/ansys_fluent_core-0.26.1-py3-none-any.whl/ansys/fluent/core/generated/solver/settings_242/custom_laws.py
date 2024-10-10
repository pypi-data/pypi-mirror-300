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

from .law_1 import law_1 as law_1_cls
from .law_2 import law_2 as law_2_cls
from .law_3 import law_3 as law_3_cls
from .law_4 import law_4 as law_4_cls
from .law_5 import law_5 as law_5_cls
from .law_6 import law_6 as law_6_cls
from .law_7 import law_7 as law_7_cls
from .law_8 import law_8 as law_8_cls
from .law_9 import law_9 as law_9_cls
from .law_10 import law_10 as law_10_cls
from .switch import switch as switch_cls

class custom_laws(Group):
    """
    'custom_laws' child.
    """

    fluent_name = "custom-laws"

    child_names = \
        ['law_1', 'law_2', 'law_3', 'law_4', 'law_5', 'law_6', 'law_7',
         'law_8', 'law_9', 'law_10', 'switch']

    _child_classes = dict(
        law_1=law_1_cls,
        law_2=law_2_cls,
        law_3=law_3_cls,
        law_4=law_4_cls,
        law_5=law_5_cls,
        law_6=law_6_cls,
        law_7=law_7_cls,
        law_8=law_8_cls,
        law_9=law_9_cls,
        law_10=law_10_cls,
        switch=switch_cls,
    )

