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

from .interaction import interaction as interaction_cls
from .unsteady_tracking import unsteady_tracking as unsteady_tracking_cls
from .contour_plotting import contour_plotting as contour_plotting_cls

class general_settings(Group):
    """
    Main menu to allow users to set options controlling:
    
     - the optional generation of averaged dpm variables on the fluid mesh to be used for post-processing,
     - the interaction between the discrete particles and their carrier phase,
     - the handling of unsteady particles.
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "general-settings"

    child_names = \
        ['interaction', 'unsteady_tracking', 'contour_plotting']

    _child_classes = dict(
        interaction=interaction_cls,
        unsteady_tracking=unsteady_tracking_cls,
        contour_plotting=contour_plotting_cls,
    )

