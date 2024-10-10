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

from .model_4 import model as model_cls
from .number_of_splashed_drops import number_of_splashed_drops as number_of_splashed_drops_cls
from .regime_parameters import regime_parameters as regime_parameters_cls

class impingement_splashing(Group):
    """
    Wall-film model impingement / splashing parameters.
    """

    fluent_name = "impingement-splashing"

    child_names = \
        ['model', 'number_of_splashed_drops', 'regime_parameters']

    _child_classes = dict(
        model=model_cls,
        number_of_splashed_drops=number_of_splashed_drops_cls,
        regime_parameters=regime_parameters_cls,
    )

    _child_aliases = dict(
        dpm_film_splash_nsamp="number_of_splashed_drops",
        dpm_imping_splash_model="model",
    )

