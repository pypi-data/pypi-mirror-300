import os

def save_transition_matrices(matrices, name, newick_with_labels_str):
    """
    Saves the transition matrices and prints them.
    """
    real_matrices = []
    output_dir = './output_files'
    # Check if the directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = "./output_files/" + name + "_transition_matrices.txt"
    with open(output_file, "w") as f:
        f.write(newick_with_labels_str + "\n")
        for m in matrices:
            f.write(m.edge[0].name + " " + m.edge[1].name + "\n")
            f.write(str(m.transition_matrix) + "\n")
            f.write("**********************************************************************\n")
    return real_matrices