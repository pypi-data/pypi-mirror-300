import numpy as np

from GenPhylo.model.matrix_computation import get_M1, get_M2
from GenPhylo.model.model_utils import find_k


def generate_random_matrix(distribution, l):
    """
    Returns the transition matrix M=M1M2 given a branch length
    and the distribution at the ancestor node.
    """

    D = np.diag(distribution)
    sq_det_D = np.sqrt(np.linalg.det(D))
    exp_minus_l = np.exp(-l)
    k = find_k(distribution, l, sq_det_D, exp_minus_l)
    dir_constant = (k*np.exp(-l/4))/(np.sqrt(l/4))

    M1, detM1, res, new_distribution = get_M1(distribution, dir_constant, exp_minus_l, sq_det_D)
    d2 = res * (1 / detM1)
    M2 = get_M2(new_distribution,d2,dir_constant)

    if not isinstance(M2, np.ndarray) and M2 == 0:
        return np.zeros((4,4))
    else:
        detM2 = np.linalg.det(M2)
        assert(np.abs(detM2 - d2) < 10**-6)
        M = np.matmul(M1,M2)
        return M

