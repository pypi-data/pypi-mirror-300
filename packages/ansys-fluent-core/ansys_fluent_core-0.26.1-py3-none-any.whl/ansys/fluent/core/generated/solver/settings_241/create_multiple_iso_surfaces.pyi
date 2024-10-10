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

from typing import Union, List, Tuple

from .field_1 import field as field_cls
from .name_3 import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .zones_4 import zones as zones_cls
from .iso_value import iso_value as iso_value_cls
from .no_of_surfaces import no_of_surfaces as no_of_surfaces_cls
from .spacing import spacing as spacing_cls

class create_multiple_iso_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    field: field_cls = ...
    name: name_cls = ...
    surfaces: surfaces_cls = ...
    zones: zones_cls = ...
    iso_value: iso_value_cls = ...
    no_of_surfaces: no_of_surfaces_cls = ...
    spacing: spacing_cls = ...
    return_type = ...
