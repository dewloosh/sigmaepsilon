# -*- coding: utf-8 -*-
from .fem.mesh import FemMesh
from .fem.pointdata import PointData
from .fem.structure import Structure
from .fem.linemesh import LineMesh
from .fem.surfacemesh import SurfaceMesh
from .model.bernoulli.section import BeamSection, get_section

__version__ = "0.0.1a"

__description__ = "High-Performance Computational Mechanics in Python."