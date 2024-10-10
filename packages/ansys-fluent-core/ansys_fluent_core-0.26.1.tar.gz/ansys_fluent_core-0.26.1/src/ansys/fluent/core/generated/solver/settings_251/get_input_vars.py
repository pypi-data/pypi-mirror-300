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

from .region_name_1 import region_name as region_name_cls

class get_input_vars(Query):
    """
    Get input variables for a given region.
    
    Parameters
    ----------
        region_name : str
            Provide region name.
    
    """

    fluent_name = "get-input-vars"

    argument_names = \
        ['region_name']

    _child_classes = dict(
        region_name=region_name_cls,
    )

