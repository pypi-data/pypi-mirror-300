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

from .coupling import coupling as coupling_cls
from .helper_session_setup import helper_session_setup as helper_session_setup_cls
from .helper_session import helper_session as helper_session_cls

class set(Group):
    fluent_name = ...
    child_names = ...
    coupling: coupling_cls = ...
    helper_session_setup: helper_session_setup_cls = ...
    helper_session: helper_session_cls = ...
