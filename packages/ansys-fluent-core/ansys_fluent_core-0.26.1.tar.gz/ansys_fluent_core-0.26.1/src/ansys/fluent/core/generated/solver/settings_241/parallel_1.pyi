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

from .thread_number_control import thread_number_control as thread_number_control_cls
from .check_verbosity_1 import check_verbosity as check_verbosity_cls
from .partition_3 import partition as partition_cls
from .set_4 import set as set_cls
from .load_balance import load_balance as load_balance_cls
from .multidomain import multidomain as multidomain_cls
from .network_1 import network as network_cls
from .timer import timer as timer_cls
from .check_1 import check as check_cls
from .show_connectivity import show_connectivity as show_connectivity_cls
from .latency import latency as latency_cls
from .bandwidth import bandwidth as bandwidth_cls

class parallel(Group):
    fluent_name = ...
    child_names = ...
    thread_number_control: thread_number_control_cls = ...
    check_verbosity: check_verbosity_cls = ...
    partition: partition_cls = ...
    set: set_cls = ...
    load_balance: load_balance_cls = ...
    multidomain: multidomain_cls = ...
    network: network_cls = ...
    timer: timer_cls = ...
    command_names = ...

    def check(self, ):
        """
        Parallel check.
        """

    def show_connectivity(self, compute_node: int):
        """
        Show machine connectivity.
        
        Parameters
        ----------
            compute_node : int
                'compute_node' child.
        
        """

    def latency(self, ):
        """
        Show network latency.
        """

    def bandwidth(self, ):
        """
        Show network bandwidth.
        """

    return_type = ...
