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

from .number_of_iterations_1 import number_of_iterations as number_of_iterations_cls

class iterate(Command):
    """
    Perform a specified number of iterations.
    
    Parameters
    ----------
        number_of_iterations : int
            Set inceremtal number of Time steps.
    
    """

    fluent_name = "iterate"

    argument_names = \
        ['number_of_iterations']

    _child_classes = dict(
        number_of_iterations=number_of_iterations_cls,
    )

    return_type = "<object object at 0x7f82c58630f0>"
