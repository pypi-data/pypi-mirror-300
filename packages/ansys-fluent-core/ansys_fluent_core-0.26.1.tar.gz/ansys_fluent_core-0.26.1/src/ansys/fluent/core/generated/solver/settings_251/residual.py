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

from .equations_1 import equations as equations_cls
from .options_12 import options as options_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .reset_1 import reset as reset_cls
from .renormalize import renormalize as renormalize_cls
from .plot_1 import plot as plot_cls
from .write_1 import write as write_cls

class residual(Group):
    """
    Options for controlling residual information that the solver reports.
    """

    fluent_name = "residual"

    child_names = \
        ['equations', 'options', 'axes', 'curves']

    command_names = \
        ['reset', 'renormalize', 'plot', 'write']

    _child_classes = dict(
        equations=equations_cls,
        options=options_cls,
        axes=axes_cls,
        curves=curves_cls,
        reset=reset_cls,
        renormalize=renormalize_cls,
        plot=plot_cls,
        write=write_cls,
    )

