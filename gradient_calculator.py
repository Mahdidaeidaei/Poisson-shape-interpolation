import numpy as np

def triangle_scalar_gradient(v0, v1, v2, f_vals):
    # v0, v1, v2: 3D coordinates of triangle vertices
    # f_vals: function values at v0, v1, v2
    e1 = v1 - v0
    e2 = v2 - v0
    normal = np.cross(e1, e2)
    area2 = np.linalg.norm(normal)

    if area2 == 0:
        return np.zeros(3)  # Degenerate triangle

    n = normal / area2
    grad = (f_vals[1] - f_vals[0]) * np.cross(n, e2) + (f_vals[2] - f_vals[0]) * np.cross(e1, n)
    return grad / area2