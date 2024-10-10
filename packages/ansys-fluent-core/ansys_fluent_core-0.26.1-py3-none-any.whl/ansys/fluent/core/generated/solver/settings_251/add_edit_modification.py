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

from .mod_name import mod_name as mod_name_cls
from .mod_exists import mod_exists as mod_exists_cls
from .mod_active import mod_active as mod_active_cls
from .mod_execution_option import mod_execution_option as mod_execution_option_cls
from .mod_iterations import mod_iterations as mod_iterations_cls
from .mod_timesteps import mod_timesteps as mod_timesteps_cls
from .mod_flowtime import mod_flowtime as mod_flowtime_cls
from .mod_python import mod_python as mod_python_cls
from .mod_command import mod_command as mod_command_cls

class add_edit_modification(Command):
    """
    Define a single case modification.
    
    Parameters
    ----------
        mod_name : str
            Name of Modification.
        mod_exists : bool
            Modification Exists?.
        mod_active : bool
            Modification is Active?.
        mod_execution_option : str
            Execution Option for Transient.
        mod_iterations : int
            Modification Iterations.
        mod_timesteps : int
            Modification Time Steps.
        mod_flowtime : real
            Modification Flow Time.
        mod_python : bool
            Modification is Python?.
        mod_command : str
            Modification.
    
    """

    fluent_name = "add-edit-modification"

    argument_names = \
        ['mod_name', 'mod_exists', 'mod_active', 'mod_execution_option',
         'mod_iterations', 'mod_timesteps', 'mod_flowtime', 'mod_python',
         'mod_command']

    _child_classes = dict(
        mod_name=mod_name_cls,
        mod_exists=mod_exists_cls,
        mod_active=mod_active_cls,
        mod_execution_option=mod_execution_option_cls,
        mod_iterations=mod_iterations_cls,
        mod_timesteps=mod_timesteps_cls,
        mod_flowtime=mod_flowtime_cls,
        mod_python=mod_python_cls,
        mod_command=mod_command_cls,
    )

