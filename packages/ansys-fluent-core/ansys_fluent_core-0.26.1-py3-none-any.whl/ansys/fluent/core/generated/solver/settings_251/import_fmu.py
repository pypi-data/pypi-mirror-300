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

from .file_name_1_2 import file_name_1 as file_name_1_cls

class import_fmu(Command):
    """
    Import a FMU file.
    
    Parameters
    ----------
        file_name_1 : str
            Allows you to import FMU file.
    
    """

    fluent_name = "import-fmu"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

