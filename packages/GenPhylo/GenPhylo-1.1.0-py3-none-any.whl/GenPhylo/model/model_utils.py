import numpy as np


def alpha(new_distribution, Q, i, k):
    """
    Returns the parameter alpha of the Metropolis - Hastings algorithm
    """
    ratio = new_distribution[k] * Q[k, i] / (new_distribution[i] * Q[i, k])
    return min(1, ratio)


def find_k(distribution, l, sq_det_D, exp_minus_l):
    """
    Finds a suitable value of k to satisfy the condition
    detM1 > np.exp(-l)*np.sqrt(np.linalg.det(D_))/np.sqrt(np.linalg.det(D)).
    """
    epsilon = 1e-3  # Desired precision
    lower_bound = 2.5
    upper_bound = 25  # Adjust upper bound as needed
    
    while upper_bound - lower_bound > epsilon:
        M1 = np.zeros((4,4))
        mid = (lower_bound + upper_bound) / 2
        dir_constant_mid = (mid*np.exp(-l/4))/(np.sqrt(l/4))
        i = 0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant_mid
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                M1[i,:] = R
                i = i + 1
        
        new_distribution = np.matmul(distribution, M1)
        D_ = np.diag(new_distribution)
        detM1 = np.linalg.det(M1)
        sq_det_D_ = np.sqrt(np.linalg.det(D_))
        res = exp_minus_l * sq_det_D_ / sq_det_D

        if detM1 > res:
            upper_bound = mid
        else:
            lower_bound = mid

    return (lower_bound + upper_bound) / 2


def DLC(matrix):
    B = True
    for j in range(matrix.shape[1]):
        max_index = np.argmax(matrix[:, j])
        if max_index != j:
            B = False
    return B


def compare_equal_matrices(matrix1, matrix2):
    """
    Compares two matrices element-wise.
    """
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if matrix1[i, j] != matrix2[i, j]:
                return False
    return True