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

from .cgns_export_filetype import cgns_export_filetype as cgns_export_filetype_cls
from .cgns_mesh_type import cgns_mesh_type as cgns_mesh_type_cls
from .cgns_polyhedral_cpu_threads import cgns_polyhedral_cpu_threads as cgns_polyhedral_cpu_threads_cls
from .cgns_merge_ngons_to_single_ngon import cgns_merge_ngons_to_single_ngon as cgns_merge_ngons_to_single_ngon_cls
from .cgns_default_cellsize_changes import cgns_default_cellsize_changes as cgns_default_cellsize_changes_cls
from .cgns_enhance_poly_export_performance import cgns_enhance_poly_export_performance as cgns_enhance_poly_export_performance_cls
from .cgns_familyname import cgns_familyname as cgns_familyname_cls
from .cgns_separate_cellzones import cgns_separate_cellzones as cgns_separate_cellzones_cls

class settings(Group):
    """
    Enter the export settings menu.
    """

    fluent_name = "settings"

    child_names = \
        ['cgns_export_filetype', 'cgns_mesh_type',
         'cgns_polyhedral_cpu_threads', 'cgns_merge_ngons_to_single_ngon',
         'cgns_default_cellsize_changes',
         'cgns_enhance_poly_export_performance', 'cgns_familyname',
         'cgns_separate_cellzones']

    _child_classes = dict(
        cgns_export_filetype=cgns_export_filetype_cls,
        cgns_mesh_type=cgns_mesh_type_cls,
        cgns_polyhedral_cpu_threads=cgns_polyhedral_cpu_threads_cls,
        cgns_merge_ngons_to_single_ngon=cgns_merge_ngons_to_single_ngon_cls,
        cgns_default_cellsize_changes=cgns_default_cellsize_changes_cls,
        cgns_enhance_poly_export_performance=cgns_enhance_poly_export_performance_cls,
        cgns_familyname=cgns_familyname_cls,
        cgns_separate_cellzones=cgns_separate_cellzones_cls,
    )

