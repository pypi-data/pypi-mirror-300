import numpy as np
import sympy as sp
from sympy import symbols, Eq, solve

from GenPhylo.model.model_utils import alpha


def get_M1(distribution, dir_constant, exp_minus_l, sq_det_D):
 
    res = 1
    iteration = 1

    # Compute M1
    while res >= 1 and iteration < 50:
        M1 = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                M1[i,:] = R
                i = i + 1

        new_distribution = np.matmul(distribution,M1)
        D_ = np.diag(new_distribution)
        sq_det_D_ = np.sqrt(np.linalg.det(D_))
        res = exp_minus_l * sq_det_D_ / sq_det_D
        detM1 = np.linalg.det(M1)

        #If detM1 > res and res < 1, conditions are met. Otherwise, a new iteration.
        if detM1 <= res:
            res = 1
        
        iteration += 1
    
    return M1, detM1, res, new_distribution


def get_M2(new_distribution,d2,dir_constant):
    """
    Metropolis - Hastings implementation to get M2
    """

    P = np.zeros((4,4))
    iteration = 0
    iter = True

    while iter and iteration < 50:
        # Random Markov matrix generation
        Q = np.zeros((4,4))
        i=0
        while i<4:
            dir = np.ones(4)
            dir[i] = dir_constant
            R = np.random.dirichlet(dir)
            if R[i] > 0.3:
                Q[i,:] = R
                i = i + 1

        # Time reversible matrix generation
        for i in range(4):
            for j in range(4):
                if i == j:
                    sum = 0
                    for k in range(4):
                        if k != i:
                            sum += (Q[i,k] * (1 - alpha(new_distribution,Q,i,k)))
                    P[i,j] = Q[i,i] + sum
                else:
                    P[i,j] = Q[i,j]*alpha(new_distribution,Q,i,j)

        assert (np.abs(np.sum(new_distribution - np.matmul(new_distribution,P)))) < 10**-6
        
        # Adjust the matrix diagonalising (ensure matrix with determinant d2)
        vaps, _ = np.linalg.eig(P)
        vaps = sorted(vaps, reverse=True)
        A = symbols('A')
        eq = Eq(-d2+(((1-A)*vaps[1]+A)*((1-A)*vaps[2]+A)*((1-A)*vaps[3]+A)),0)
        sol = solve(eq, A)
        # We only want the real solution between 0 and 1
        for s in sol:
            if s.is_real and 0 <= s <= 1:
                a = np.float64(s)
                M2 = (1-a)*P + a*np.identity(4)
                iter = False
                break
            elif s.is_complex: #If imaginary part is negligible
                if np.abs(np.imag(s)) < 10**-9 and 0 <= sp.re(s) <= 1:
                    a = np.float64(sp.re(s))
                    M2 = (1-a)*P + a*np.identity(4)
                    iter = False
                    break
        iteration += 1
    
    if iteration == 50:
        return 0
    else: 
        return M2