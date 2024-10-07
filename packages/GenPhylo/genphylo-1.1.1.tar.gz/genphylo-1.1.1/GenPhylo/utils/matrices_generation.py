import numpy as np

from GenPhylo.model.math_model import generate_random_matrix
from GenPhylo.model.model_utils import DLC, compare_equal_matrices
from GenPhylo.utils.classes import Edge


def generate_transition_matrices(tree, node_distribution):
    """
    Generates transition matrices for each edge in the phylogenetic tree.
    """
    matrices = []
    for edge in tree.edges():
        l = 4 * edge[1].branch_length  # (Lake'94)
        matrix = np.zeros((4,4))
        while compare_equal_matrices(matrix, np.zeros((4,4))):
            matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        assert (np.sum(matrix) > 0)
        iter = 0 # threshold on the number of iterations for DLC matrices 
        while not DLC(matrix) and iter < 5:
            iter += 1
            matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        if iter == 5:
            print("Warning: Could not generate a DLC matrix for edge: ", edge)
        new_edge = Edge(edge, matrix)
        matrices.append(new_edge)
        node_distribution[edge[1].name] = np.matmul(node_distribution[edge[0].name], new_edge.transition_matrix)
        for i in range(4):
            assert (np.sum(new_edge.transition_matrix[i, :]) < 1.000000001 and np.sum(
                new_edge.transition_matrix[i, :]) > 0.999999999)
    return matrices