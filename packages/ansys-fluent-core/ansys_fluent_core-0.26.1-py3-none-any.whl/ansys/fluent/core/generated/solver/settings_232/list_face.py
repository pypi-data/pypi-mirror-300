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

from .face_name import face_name as face_name_cls

class list_face(Command):
    """
    'list_face' command.
    
    Parameters
    ----------
        face_name : str
            'face_name' child.
    
    """

    fluent_name = "list-face"

    argument_names = \
        ['face_name']

    _child_classes = dict(
        face_name=face_name_cls,
    )

    return_type = "<object object at 0x7fe5b915e620>"
