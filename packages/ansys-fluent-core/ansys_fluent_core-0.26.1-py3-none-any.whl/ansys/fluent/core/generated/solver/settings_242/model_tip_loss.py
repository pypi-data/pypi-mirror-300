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


class model_tip_loss(Integer):
    """
    Select Tip Loss Model:
    
     - Enter 1 if using Quadratic model 
     - Enter 2 if using modified Prandtl model 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "model-tip-loss"

