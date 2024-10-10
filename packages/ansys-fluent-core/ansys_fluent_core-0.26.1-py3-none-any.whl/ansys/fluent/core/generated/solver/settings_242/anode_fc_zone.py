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

from .anode_fc_zone_list import anode_fc_zone_list as anode_fc_zone_list_cls

class anode_fc_zone(Group):
    """
    Set up anode flow channel.
    """

    fluent_name = "anode-fc-zone"

    child_names = \
        ['anode_fc_zone_list']

    _child_classes = dict(
        anode_fc_zone_list=anode_fc_zone_list_cls,
    )

