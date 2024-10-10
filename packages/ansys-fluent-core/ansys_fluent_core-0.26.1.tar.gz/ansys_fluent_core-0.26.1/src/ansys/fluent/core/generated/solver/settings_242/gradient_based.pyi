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

from typing import Union, List, Tuple

from .observables import observables as observables_cls
from .methods_2 import methods as methods_cls
from .controls_2 import controls as controls_cls
from .monitors import monitors as monitors_cls
from .calculation import calculation as calculation_cls
from .postprocess_options import postprocess_options as postprocess_options_cls
from .reporting import reporting as reporting_cls
from .design_tool import design_tool as design_tool_cls
from .optimizer import optimizer as optimizer_cls
from .enable_21 import enable as enable_cls

class gradient_based(Group):
    fluent_name = ...
    child_names = ...
    observables: observables_cls = ...
    methods: methods_cls = ...
    controls: controls_cls = ...
    monitors: monitors_cls = ...
    calculation: calculation_cls = ...
    postprocess_options: postprocess_options_cls = ...
    reporting: reporting_cls = ...
    design_tool: design_tool_cls = ...
    optimizer: optimizer_cls = ...
    command_names = ...

    def enable(self, ):
        """
        Enables and loads adjoint module.
        """

