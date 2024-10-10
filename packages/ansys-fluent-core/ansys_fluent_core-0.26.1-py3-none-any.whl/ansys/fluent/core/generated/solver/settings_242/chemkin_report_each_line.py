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

from .report_each_line import report_each_line as report_each_line_cls

class chemkin_report_each_line(Command):
    """
    Choose whether or not to report after reading each line.
    
    Parameters
    ----------
        report_each_line : bool
            Enable/disable reporting after reading each line.
    
    """

    fluent_name = "chemkin-report-each-line?"

    argument_names = \
        ['report_each_line']

    _child_classes = dict(
        report_each_line=report_each_line_cls,
    )

