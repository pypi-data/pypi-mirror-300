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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .inert_particle_child import inert_particle_child


class inert_particle(NamedObject[inert_particle_child], CreatableNamedObjectMixinOld[inert_particle_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : str
                'to' child.
        
        """

    child_object_type: inert_particle_child = ...
    return_type = ...
