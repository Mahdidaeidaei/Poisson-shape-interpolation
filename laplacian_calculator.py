from scipy.sparse import lil_matrix
import numpy as np

def cotangent_laplacian(V, F):
    n = V.shape[0]
    L = lil_matrix((n, n))

    for tri in F:
        i, j, k = tri
        vi, vj, vk = V[i], V[j], V[k]

        # Compute cotangents of angles
        def cotangent(a, b):
            cos_theta = np.dot(a, b)
            sin_theta = np.linalg.norm(np.cross(a, b))
            return cos_theta / sin_theta if sin_theta > 1e-8 else 0.0

        # Compute edge vectors and cotangent weights
        cot_alpha = cotangent(vj - vi, vk - vi)  # angle at vi
        cot_beta  = cotangent(vk - vj, vi - vj)  # angle at vj
        cot_gamma = cotangent(vi - vk, vj - vk)  # angle at vk

        # Add contributions symmetrically
        for (u, v, w) in [(i, j, cot_gamma), (j, k, cot_alpha), (k, i, cot_beta)]:
            L[u, v] -= 0.5 * w
            L[v, u] -= 0.5 * w
            L[u, u] += 0.5 * w
            L[v, v] += 0.5 * w

    return L.tocsr()