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

from .axes_2 import axes as axes_cls
from .main import main as main_cls
from .scale_3 import scale as scale_cls
from .text import text as text_cls
from .video import video as video_cls
from .xy import xy as xy_cls
from .logo import logo as logo_cls
from .ruler_1 import ruler as ruler_cls
from .logo_color import logo_color as logo_color_cls
from .aspect_ratio import aspect_ratio as aspect_ratio_cls

class windows(Group):
    fluent_name = ...
    child_names = ...
    axes: axes_cls = ...
    main: main_cls = ...
    scale: scale_cls = ...
    text: text_cls = ...
    video: video_cls = ...
    xy: xy_cls = ...
    logo: logo_cls = ...
    ruler: ruler_cls = ...
    logo_color: logo_color_cls = ...
    command_names = ...

    def aspect_ratio(self, width: float | str, height: float | str):
        """
        Set the aspect ratio of the active window.
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        
        """

    return_type = ...
