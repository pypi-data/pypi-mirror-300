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

from .fluid_1 import fluid as fluid_cls
from .solid_1 import solid as solid_cls
from .change_type import change_type as change_type_cls
from .activate_cell_zone import activate_cell_zone as activate_cell_zone_cls
from .mrf_to_sliding_mesh import mrf_to_sliding_mesh as mrf_to_sliding_mesh_cls
from .convert_all_solid_mrf_to_solid_motion import convert_all_solid_mrf_to_solid_motion as convert_all_solid_mrf_to_solid_motion_cls
from .copy_mrf_to_mesh_motion import copy_mrf_to_mesh_motion as copy_mrf_to_mesh_motion_cls
from .copy_mesh_to_mrf_motion import copy_mesh_to_mrf_motion as copy_mesh_to_mrf_motion_cls

class cell_zone_conditions(Group, _ChildNamedObjectAccessorMixin):
    """
    'cell_zone_conditions' child.
    """

    fluent_name = "cell-zone-conditions"

    child_names = \
        ['fluid', 'solid']

    command_names = \
        ['change_type', 'activate_cell_zone', 'mrf_to_sliding_mesh',
         'convert_all_solid_mrf_to_solid_motion', 'copy_mrf_to_mesh_motion',
         'copy_mesh_to_mrf_motion']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
        change_type=change_type_cls,
        activate_cell_zone=activate_cell_zone_cls,
        mrf_to_sliding_mesh=mrf_to_sliding_mesh_cls,
        convert_all_solid_mrf_to_solid_motion=convert_all_solid_mrf_to_solid_motion_cls,
        copy_mrf_to_mesh_motion=copy_mrf_to_mesh_motion_cls,
        copy_mesh_to_mrf_motion=copy_mesh_to_mrf_motion_cls,
    )

    return_type = "<object object at 0x7ff9d1766920>"
