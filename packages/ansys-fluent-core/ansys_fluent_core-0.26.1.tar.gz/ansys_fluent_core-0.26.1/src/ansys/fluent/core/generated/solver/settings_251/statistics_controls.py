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

from .method_3 import method as method_cls
from .samp_time_period import samp_time_period as samp_time_period_cls
from .samp_time_steps import samp_time_steps as samp_time_steps_cls
from .avg_time_period import avg_time_period as avg_time_period_cls
from .avg_time_steps import avg_time_steps as avg_time_steps_cls

class statistics_controls(Command):
    """
    Specify statistics parameters of sampling and averaging of flow and optical quantities.
    
    Parameters
    ----------
        method : int
            'method' child.
        samp_time_period : real
            'samp_time_period' child.
        samp_time_steps : int
            'samp_time_steps' child.
        avg_time_period : real
            'avg_time_period' child.
        avg_time_steps : int
            'avg_time_steps' child.
    
    """

    fluent_name = "statistics-controls"

    argument_names = \
        ['method', 'samp_time_period', 'samp_time_steps', 'avg_time_period',
         'avg_time_steps']

    _child_classes = dict(
        method=method_cls,
        samp_time_period=samp_time_period_cls,
        samp_time_steps=samp_time_steps_cls,
        avg_time_period=avg_time_period_cls,
        avg_time_steps=avg_time_steps_cls,
    )

