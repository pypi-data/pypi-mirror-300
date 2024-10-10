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

from .display import display as display_cls
from .particle_tracks_child import particle_tracks_child


class particle_tracks(NamedObject[particle_tracks_child], CreatableNamedObjectMixinOld[particle_tracks_child]):
    fluent_name = ...
    command_names = ...

    def display(self, object_name: str):
        """
        'display' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    child_object_type: particle_tracks_child = ...
    return_type = ...
