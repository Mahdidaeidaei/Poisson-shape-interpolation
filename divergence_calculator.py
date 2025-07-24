import numpy as np


def compute_divergence(V, F, G):
    n = V.shape[0]
    b = np.zeros(n)

    for i, tri in enumerate(F):
        idx0, idx1, idx2 = tri
        v0, v1, v2 = V[idx0], V[idx1], V[idx2]

        # Face area and normal
        N = np.cross(v1 - v0, v2 - v0)
        area = 0.5 * np.linalg.norm(N)
        if area < 1e-10:
            continue

        # Normalized face normal
        N = N / (2 * area)

        # Compute gradients of basis functions (ϕ0, ϕ1, ϕ2)
        grad_phi = np.zeros((3, 3))
        grad_phi[0] = np.cross(N, v2 - v1)
        grad_phi[1] = np.cross(N, v0 - v2)
        grad_phi[2] = np.cross(N, v1 - v0)

        for local_idx, global_idx in enumerate(tri):
            b[global_idx] += np.dot(G[i], grad_phi[local_idx]) / 2

    return b
