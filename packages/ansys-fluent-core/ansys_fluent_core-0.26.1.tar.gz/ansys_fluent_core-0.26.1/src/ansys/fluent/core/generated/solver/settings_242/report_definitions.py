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

from .mesh_1 import mesh as mesh_cls
from .surface_1 import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .time_1 import time as time_cls
from .flux_1 import flux as flux_cls
from .vbm import vbm as vbm_cls
from .injection_1 import injection as injection_cls
from .user_defined_6 import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .icing_3 import icing as icing_cls
from .expression_1 import expression as expression_cls
from .single_valued_expression import single_valued_expression as single_valued_expression_cls
from .custom import custom as custom_cls
from .compute_2 import compute as compute_cls
from .copy_2 import copy as copy_cls

class report_definitions(Group, _ChildNamedObjectAccessorMixin):
    """
    Provides access to create an object that specifies a certain quantity or set of values to be computed at the end of a solver timestep or iteration. You can then choose to have multiple report definitions printed to the console written to a single file or plotted in the same window.
    """

    fluent_name = "report-definitions"

    child_names = \
        ['mesh', 'surface', 'volume', 'force', 'lift', 'drag', 'moment',
         'time', 'flux', 'vbm', 'injection', 'user_defined', 'aeromechanics',
         'icing', 'expression', 'single_valued_expression', 'custom']

    command_names = \
        ['compute', 'copy']

    _child_classes = dict(
        mesh=mesh_cls,
        surface=surface_cls,
        volume=volume_cls,
        force=force_cls,
        lift=lift_cls,
        drag=drag_cls,
        moment=moment_cls,
        time=time_cls,
        flux=flux_cls,
        vbm=vbm_cls,
        injection=injection_cls,
        user_defined=user_defined_cls,
        aeromechanics=aeromechanics_cls,
        icing=icing_cls,
        expression=expression_cls,
        single_valued_expression=single_valued_expression_cls,
        custom=custom_cls,
        compute=compute_cls,
        copy=copy_cls,
    )

