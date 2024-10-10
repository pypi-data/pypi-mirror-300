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

from .type_2 import type as type_cls
from .formula import formula as formula_cls
from .new_name_1 import new_name as new_name_cls
from .new_formula import new_formula as new_formula_cls

class copy_by_formula(Command):
    """
    Copy database material by formula.
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
        new_name : str
            Material with same name exist. Please select new material name.
        new_formula : str
            Material with same chemical formula exist. Please select new chemical formula.
    
    """

    fluent_name = "copy-by-formula"

    argument_names = \
        ['type', 'formula', 'new_name', 'new_formula']

    _child_classes = dict(
        type=type_cls,
        formula=formula_cls,
        new_name=new_name_cls,
        new_formula=new_formula_cls,
    )

