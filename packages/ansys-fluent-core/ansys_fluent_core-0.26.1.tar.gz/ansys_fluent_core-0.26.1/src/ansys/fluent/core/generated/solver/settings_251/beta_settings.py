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

from .enable import enable as enable_cls

class beta_settings(Command):
    """
    Enable access to beta features in the interface.
    
    Parameters
    ----------
        enable : bool
            Enable or disable beta features.
    
    """

    fluent_name = "beta-settings"

    argument_names = \
        ['enable']

    _child_classes = dict(
        enable=enable_cls,
    )

