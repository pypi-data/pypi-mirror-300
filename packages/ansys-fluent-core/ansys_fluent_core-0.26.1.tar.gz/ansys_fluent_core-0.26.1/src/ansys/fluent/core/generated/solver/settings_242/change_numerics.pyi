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

from .use_sided_area_vector import use_sided_area_vector as use_sided_area_vector_cls
from .use_nci_sided_area_vectors import use_nci_sided_area_vectors as use_nci_sided_area_vectors_cls
from .recreate import recreate as recreate_cls

class change_numerics(Command):
    fluent_name = ...
    argument_names = ...
    use_sided_area_vector: use_sided_area_vector_cls = ...
    use_nci_sided_area_vectors: use_nci_sided_area_vectors_cls = ...
    recreate: recreate_cls = ...
