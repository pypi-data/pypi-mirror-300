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

from .particle_drag import particle_drag as particle_drag_cls
from .particle_rotation import particle_rotation as particle_rotation_cls
from .heat_transfer import heat_transfer as heat_transfer_cls
from .custom_laws import custom_laws as custom_laws_cls
from .turbulent_dispersion import turbulent_dispersion as turbulent_dispersion_cls
from .droplet_breakup import droplet_breakup as droplet_breakup_cls

class physical_models(Group):
    fluent_name = ...
    child_names = ...
    particle_drag: particle_drag_cls = ...
    particle_rotation: particle_rotation_cls = ...
    heat_transfer: heat_transfer_cls = ...
    custom_laws: custom_laws_cls = ...
    turbulent_dispersion: turbulent_dispersion_cls = ...
    droplet_breakup: droplet_breakup_cls = ...
    return_type = ...
