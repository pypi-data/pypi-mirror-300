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

from .kw_low_re_correction import kw_low_re_correction as kw_low_re_correction_cls
from .kw_shear_correction import kw_shear_correction as kw_shear_correction_cls
from .turb_compressibility import turb_compressibility as turb_compressibility_cls

class k_omega_options(Group):
    """
    'k_omega_options' child.
    """

    fluent_name = "k-omega-options"

    child_names = \
        ['kw_low_re_correction', 'kw_shear_correction',
         'turb_compressibility']

    _child_classes = dict(
        kw_low_re_correction=kw_low_re_correction_cls,
        kw_shear_correction=kw_shear_correction_cls,
        turb_compressibility=turb_compressibility_cls,
    )

    return_type = "<object object at 0x7ff9d2a0d840>"
