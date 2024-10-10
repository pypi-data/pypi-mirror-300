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

from .report_defs import report_defs as report_defs_cls

class compute(Command):
    """
    'compute' command.
    
    Parameters
    ----------
        report_defs : List
            'report_defs' child.
    
    """

    fluent_name = "compute"

    argument_names = \
        ['report_defs']

    _child_classes = dict(
        report_defs=report_defs_cls,
    )

    return_type = "<object object at 0x7ff9d0a61230>"
