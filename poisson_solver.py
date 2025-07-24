from scipy.sparse.linalg import spsolve


def solve_poisson_with_constraint(L, b, fixed_index=0, fixed_value=0.0):
    n = L.shape[0]

    # Replace one row in L to fix a value
    L = L.tolil()
    L[fixed_index, :] = 0
    L[fixed_index, fixed_index] = 1
    b[fixed_index] = fixed_value

    return spsolve(L.tocsr(), b)