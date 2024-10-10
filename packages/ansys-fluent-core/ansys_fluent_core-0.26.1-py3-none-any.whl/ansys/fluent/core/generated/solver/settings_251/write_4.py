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

from .filename_1_3 import filename_1 as filename_1_cls

class write(Command):
    """
    Write a histogram of a scalar quantity to a file.
    
    Parameters
    ----------
        filename_1 : str
            Enter the name you want the file saved with.
    
    """

    fluent_name = "write"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_1_cls,
    )

