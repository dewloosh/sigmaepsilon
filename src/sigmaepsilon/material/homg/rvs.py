from typing import Iterable, Union

import numpy as np

from neumann.linalg import CartesianFrame

from ...utils.fem.ebc import link_opposite_sides
from .utils import ( 
    _strain_field_3d_bulk,
    _postproc_3d_gauss_stresses,
    _postproc_shell_gauss_dynams,
    _calc_avg_hooke_3d_to_shell,
    _calc_avg_hooke_shell,
    _transform_3d_strain_loads_to_surfaces,
    )
from sigmaepsilon.fem import FemMesh, Structure
from sigmaepsilon.fem.ebc import NodeToNode


class RepresentativeSurfaceElement(Structure):
    
    @staticmethod
    def periodic_essential_ebc(
        mesh: FemMesh,
        axis: Union[int, Iterable[int]] = 0
    ) -> NodeToNode:
        imap = link_opposite_sides(mesh.points(), axis)
        return NodeToNode(imap)
       
    def ABD(self):
        """
        Returns the elasticity matrix for a Kirchhoff-Love plate.
        """
        return self.homogenize(model='KL')    
    
    def ABDS(self):
        """
        Returns the elasticity matrix for a Mindlin-Reissner plate.
        """
        return self.homogenize(model='MR')
    
    def homogenize(self, model:str='MR'):
        """
        Returns the homogenized elasticity matrix for a Mindlin-Reissner or a
        Kirchhoff-Love plate.
        """
        mesh = self.mesh
        NDOFN = mesh.NDOFN
        
        if model.lower() == 'mr':
            NSTRE = 8
        elif model.lower() == 'kl':
            NSTRE = 6
            
        # mesh data
        points = mesh.points()
        [(xmin, xmax), (ymin, ymax), (_, _)] = points.bounds()
        center = points.center()
        area = (xmax - xmin) * (ymax - ymin)
        
        # nodal loads
        nodal_loads = np.zeros((len(points), NDOFN, NSTRE), dtype=float)
        mesh.pd.loads = nodal_loads
        
        # nodal supports against rigid body motion
        nodal_fixity = np.zeros((len(points), NDOFN), dtype=bool)
        i = points.index_of_closest(center)
        nodal_fixity[i, :3] = True
        i = points.index_of_closest([xmax, 0, 0])
        nodal_fixity[i, [1, 2]] = True
        i = points.index_of_closest([0, ymax, 0])
        nodal_fixity[i, 2] = True
        mesh.pd.fixity = nodal_fixity
        
        # nodal supports to guarantee peridic displacement solution
        periodicity_constraints = self.periodic_essential_ebc(mesh, axis=[0, 1])
        
        # initial strain loads
        blocks = list(mesh.cellblocks(inclusive=True))
        for block in blocks:
            centers = block.centers()
            strain_loads = np.zeros((centers.shape[0], 6, NSTRE))
            _strain_field_3d_bulk(centers, out=strain_loads, NSTRE=NSTRE)
            if block.cd.NDIM == 3:        
                block.cd.strain_loads = strain_loads
            elif block.cd.NDIM == 2:
                surface_frames = CartesianFrame(block.cd.frames, assume_cartesian=True)
                strain_loads = _transform_3d_strain_loads_to_surfaces(
                    strain_loads, 
                    surface_frames
                )
                block.cd.strain_loads = strain_loads
            else:
                raise NotImplementedError
        
        # solve BVP
        #self.clear_constraints()
        self.constraints.append(periodicity_constraints)
        self.linear_static_analysis()
        
        # postproc
        hooke = np.zeros((NSTRE, NSTRE), dtype=float)
        hooke_avg = np.zeros_like(hooke)
        for block in blocks:
            block.cd.strain_loads = None
            hooke_block = block.cd.elastic_material_stiffness_matrix()
            gp, gw = block.cd.quadrature["full"]
            #cell_forces = block.internal_forces(points=gp, flatten=False, target='global') 
            if block.cd.NDIM == 3: 
                cell_forces = block.internal_forces(points=gp, flatten=False, target='global')        
                ec = block.cells_coords()
                dshp = block.cd.shape_function_derivatives(gp)
                jac = block.cd.jacobian_matrix(dshp=dshp, ecoords=ec)
                djac = block.cd.jacobian(jac=jac)
                ec = block.cells_coords(points=gp)
                _postproc_3d_gauss_stresses(cell_forces, ec, gw, djac, hooke)     
                _calc_avg_hooke_3d_to_shell(hooke_block, ec, gw, djac, hooke_avg)
            elif block.cd.NDIM == 2:
                cell_forces = block.internal_forces(points=gp, flatten=False, target='global') 
                ec = block.cells_coords()
                dshp = block.cd.shape_function_derivatives(gp)
                jac = block.cd.jacobian_matrix(dshp=dshp, ecoords=ec)
                djac = block.cd.jacobian(jac=jac)
                _postproc_shell_gauss_dynams(cell_forces, gw, djac, hooke)
                _calc_avg_hooke_shell(hooke_block, block.cd.areas(), hooke_avg)
            else:
                raise NotImplementedError
        
        hooke /= area
        hooke_avg /= area
        result = hooke_avg - hooke
        if NSTRE == 8:
            result[6:8, 6:8] = hooke[6:8, 6:8] * 5/6       
        return result        
    
    