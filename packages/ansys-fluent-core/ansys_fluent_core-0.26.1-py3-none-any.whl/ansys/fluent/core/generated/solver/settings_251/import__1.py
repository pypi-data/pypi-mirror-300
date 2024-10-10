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

from .tsv_file_name_1 import tsv_file_name_1 as tsv_file_name_1_cls

class import_(Command):
    """
    Import execute-commands from a TSV file.
    
    Parameters
    ----------
        tsv_file_name_1 : str
            'tsv_file_name' child.
    
    """

    fluent_name = "import_"

    argument_names = \
        ['tsv_file_name']

    _child_classes = dict(
        tsv_file_name=tsv_file_name_1_cls,
    )

