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

from .path_1 import path_1 as path_1_cls
from .filename import filename as filename_cls
from .extension import extension as extension_cls

class outline_view_settings(Command):
    """
    Export case settings by providing the location of those settings in the Outline View tree.
    
    Parameters
    ----------
        path_1 : str
            Export case settings by providing the location of those settings in the Outline View Tree.
     For example, "setup/models/viscous" will export the settings of the viscous turbulence model.
        filename : str
            Enter Filename for exported file.
        extension : str
            Enter extension to export the file.
    
    """

    fluent_name = "outline-view-settings"

    argument_names = \
        ['path_1', 'filename', 'extension']

    _child_classes = dict(
        path_1=path_1_cls,
        filename=filename_cls,
        extension=extension_cls,
    )

