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

from .camera import camera as camera_cls
from .display_states import display_states as display_states_cls
from .rendering_options import rendering_options as rendering_options_cls
from .mirror_planes import mirror_planes as mirror_planes_cls
from .mirror_zones import mirror_zones as mirror_zones_cls
from .auto_scale_3 import auto_scale as auto_scale_cls
from .reset_to_default_view import reset_to_default_view as reset_to_default_view_cls
from .delete_view import delete_view as delete_view_cls
from .last_view import last_view as last_view_cls
from .next_view import next_view as next_view_cls
from .list_views import list_views as list_views_cls
from .restore_view import restore_view as restore_view_cls
from .read_views import read_views as read_views_cls
from .save_view import save_view as save_view_cls
from .write_views import write_views as write_views_cls
from .apply_mirror_planes import apply_mirror_planes as apply_mirror_planes_cls
from .get_current_mirror_planes import get_current_mirror_planes as get_current_mirror_planes_cls

class views(Group):
    """
    'views' child.
    """

    fluent_name = "views"

    child_names = \
        ['camera', 'display_states', 'rendering_options', 'mirror_planes',
         'mirror_zones']

    command_names = \
        ['auto_scale', 'reset_to_default_view', 'delete_view', 'last_view',
         'next_view', 'list_views', 'restore_view', 'read_views', 'save_view',
         'write_views', 'apply_mirror_planes']

    query_names = \
        ['get_current_mirror_planes']

    _child_classes = dict(
        camera=camera_cls,
        display_states=display_states_cls,
        rendering_options=rendering_options_cls,
        mirror_planes=mirror_planes_cls,
        mirror_zones=mirror_zones_cls,
        auto_scale=auto_scale_cls,
        reset_to_default_view=reset_to_default_view_cls,
        delete_view=delete_view_cls,
        last_view=last_view_cls,
        next_view=next_view_cls,
        list_views=list_views_cls,
        restore_view=restore_view_cls,
        read_views=read_views_cls,
        save_view=save_view_cls,
        write_views=write_views_cls,
        apply_mirror_planes=apply_mirror_planes_cls,
        get_current_mirror_planes=get_current_mirror_planes_cls,
    )

