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

from .verbosity_option import verbosity_option as verbosity_option_cls

class mphase_summary(Command):
    """
    Multiphase Summary and Recommendations.
    
    Parameters
    ----------
        verbosity_option : str
            'verbosity_option' child.
    
    """

    fluent_name = "mphase-summary"

    argument_names = \
        ['verbosity_option']

    _child_classes = dict(
        verbosity_option=verbosity_option_cls,
    )

    return_type = "<object object at 0x7fe5b8e2f5d0>"
