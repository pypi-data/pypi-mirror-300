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

from .key import key as key_cls

class add_keyframe(Command):
    """
    Add keyframe.
    
    Parameters
    ----------
        key : int
            'key' child.
    
    """

    fluent_name = "add-keyframe"

    argument_names = \
        ['key']

    _child_classes = dict(
        key=key_cls,
    )

