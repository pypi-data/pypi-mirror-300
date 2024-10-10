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

from .change_numerics import change_numerics as change_numerics_cls

class non_conformal_interface_numerics(Group):
    fluent_name = ...
    command_names = ...

    def change_numerics(self, use_sided_area_vector: bool, use_nci_sided_area_vectors: bool, recreate: bool):
        """
        Enable modified non-conformal interface numerics.
        
        Parameters
        ----------
            use_sided_area_vector : bool
                'use_sided_area_vector' child.
            use_nci_sided_area_vectors : bool
                'use_nci_sided_area_vectors' child.
            recreate : bool
                'recreate' child.
        
        """

    return_type = ...
