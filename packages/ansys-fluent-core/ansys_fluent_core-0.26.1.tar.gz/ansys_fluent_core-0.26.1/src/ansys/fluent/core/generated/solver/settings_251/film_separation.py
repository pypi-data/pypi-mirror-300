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

from .model_5 import model as model_cls
from .critical_weber_number_1 import critical_weber_number as critical_weber_number_cls
from .separation_angle import separation_angle as separation_angle_cls

class film_separation(Group):
    """
    Wall film separation model parameters.
    """

    fluent_name = "film-separation"

    child_names = \
        ['model', 'critical_weber_number', 'separation_angle']

    _child_classes = dict(
        model=model_cls,
        critical_weber_number=critical_weber_number_cls,
        separation_angle=separation_angle_cls,
    )

    _child_aliases = dict(
        dpm_critical_we_number="critical_weber_number",
        dpm_film_separation_angle="separation_angle",
        dpm_film_separation_model="model",
    )

