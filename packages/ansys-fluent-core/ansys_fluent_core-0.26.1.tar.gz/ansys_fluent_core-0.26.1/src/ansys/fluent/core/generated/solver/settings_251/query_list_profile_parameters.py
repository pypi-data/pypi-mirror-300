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

from .profile_name_1 import profile_name as profile_name_cls

class query_list_profile_parameters(Query):
    """
    Query-list-profile-parameters-class.
    
    Parameters
    ----------
        profile_name : str
            Profile name.
    
    """

    fluent_name = "query-list-profile-parameters"

    argument_names = \
        ['profile_name']

    _child_classes = dict(
        profile_name=profile_name_cls,
    )

