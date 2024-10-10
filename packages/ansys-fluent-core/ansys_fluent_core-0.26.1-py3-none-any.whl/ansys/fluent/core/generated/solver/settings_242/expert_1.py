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

from .randomize_every_iteration import randomize_every_iteration as randomize_every_iteration_cls
from .randomize_every_timestep import randomize_every_timestep as randomize_every_timestep_cls
from .tracking_statistics_format import tracking_statistics_format as tracking_statistics_format_cls
from .verbosity_1 import verbosity as verbosity_cls
from .reference_frame import reference_frame as reference_frame_cls

class expert(Group):
    """
    Menu containing not frequently used (expert level) settings.
    """

    fluent_name = "expert"

    child_names = \
        ['randomize_every_iteration', 'randomize_every_timestep',
         'tracking_statistics_format', 'verbosity', 'reference_frame']

    _child_classes = dict(
        randomize_every_iteration=randomize_every_iteration_cls,
        randomize_every_timestep=randomize_every_timestep_cls,
        tracking_statistics_format=tracking_statistics_format_cls,
        verbosity=verbosity_cls,
        reference_frame=reference_frame_cls,
    )

