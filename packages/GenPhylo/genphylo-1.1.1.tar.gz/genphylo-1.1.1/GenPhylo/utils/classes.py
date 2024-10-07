class Edge:
    def __init__(self, edge, transition_matrix=None):
        self.edge = edge
        self.transition_matrix = transition_matrix

class MM:
    def __init__(self, source, target, matrix):
        self.source = source
        self.target = target
        self.matrix = matrix