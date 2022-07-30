# -*- coding: utf-8 -*-
from numba import njit, prange
import numpy as np
from numpy import ndarray

from ..cells.utils import element_dof_solution_bulk

__cache = True


@njit(nogil=True, parallel=True, cache=__cache)
def model_strains(dofsol1d: ndarray, gnum: ndarray, B: ndarray):
    nE, nP, NSTRE = B.shape[:3]
    esol = element_dof_solution_bulk(dofsol1d, gnum)
    res = np.zeros((nE, nP, NSTRE), dtype=dofsol1d.dtype)
    for iE in prange(nE):
        for iP in prange(nP):
            res[iE, iP, :] = B[iE, iP] @ esol[iE]
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def stresses_from_strains(C: ndarray, strains: ndarray):
    nE, nP, _ = strains.shape
    res = np.zeros_like(strains)
    for iE in prange(nE):
        for iP in prange(nP):
            res[iE, iP, :] = C[iE] @ strains[iE, iP]
    return res
