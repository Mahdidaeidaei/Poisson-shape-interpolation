import numpy as np


def compute_gradient_field_with_normals(V, F):
    G = np.zeros((F.shape[0], 3, 3))  # (n_faces, coord, gradient vector in local frame)
    Df = np.zeros((F.shape[0], 3, 3))

    for i, tri in enumerate(F):
        v0, v1, v2 = V[tri[0]], V[tri[1]], V[tri[2]]

        # Construct local frame: edge1, edge2, normal
        e1 = v1 - v0
        e2 = v2 - v0
        n = np.cross(e1, e2)
        n_norm = np.linalg.norm(n)
        if n_norm < 1e-8:
            continue  # skip degenerate triangle
        n /= n_norm
        frame = np.stack([e1, e2, n], axis=0)  # shape (3,3)
        
        try:
            inv_frame = np.linalg.inv(frame)  # (3,3)
        except np.linalg.LinAlgError:
            continue

        for coord in range(3):  # for x, y, z
            # Values at triangle vertices for this coordinate
            values = [v0[coord], v1[coord], v2[coord]]
            df = np.array([values[1] - values[0], values[2] - values[0], 0.0])  # (3,)
            # Compute gradient in local frame
            grad_local = inv_frame @ df  # (3,)
            Df[i,coord] = df
            G[i, coord] = grad_local
    
    return G , Df  # Shape: (n_faces, 3, 3)