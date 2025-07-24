import numpy as np
from scipy.spatial.transform import Rotation as R, Slerp

def nonlinear_gradient_interpolation(Df0, Df1, V0, V1, F, t):
    G_interp = np.zeros_like(Df0)

    for i, tri in enumerate(F):

        idx0, idx1, idx2 = tri
        v0_0, v1_0, v2_0 = V0[idx0], V0[idx1], V0[idx2]
        v0_1, v1_1, v2_1 = V1[idx0], V1[idx1], V1[idx2]

        # Construct affine frames: 2 edge vectors and normal
        def affine_frame(v0, v1, v2):
            e1 = v1 - v0
            e2 = v2 - v0
            n = np.cross(e1, e2)
            n_norm = np.linalg.norm(n)
            if n_norm < 1e-8:
                n = np.zeros(3)
            else:
                n /= n_norm
            return np.stack([e1, e2, n], axis=0)  # 3x3 matrix

        F0 = affine_frame(v0_0, v1_0, v2_0)
        F1 = affine_frame(v0_1, v1_1, v2_1)

        if np.linalg.matrix_rank(F0) < 3:
            continue  # skip degenerate

        #H = F1 @ np.linalg.inv(F0)
        H =  np.linalg.inv(F1) @ F0

        M = Df1[i] @ np.linalg.pinv(Df0[i])

        """
        print(Df1[i])
        #print(M @ Df0[i])
        #print(Df1[i] - M @ Df0[i])

        for coord in range(3):

            print(Df1[i , coord])
            C = M @ Df0[i]
            #print( C[coord])
            
        break
        """
        #************************************************************************************
        # Polar decomposition: H = R @ S
        U, sigma, VT = np.linalg.svd(H)
        R_mat = U @ VT
        if np.linalg.det(R_mat) < 0:
            VT[2, :] *= -1
            R_mat = U @ VT
        S_mat = VT.T @ np.diag(sigma) @ VT

        # SLERP on R: convert to quaternion and interpolate
        # SLERP on R: interpolate rotation using quaternions
        key_times = [0, 1]
        key_rots = R.from_matrix([np.eye(3), R_mat])
        slerp = Slerp(key_times, key_rots)
        R_t = slerp(t).as_matrix()

        # Interpolate stretch
        S_t = (1-t) * np.eye(3) + t * S_mat

        # H_t = R_t @ S_t
        H_t = R_t @ S_t
        #*************************************************************************************
        # Polar decomposition: H = R @ S
        U, sigma, VT = np.linalg.svd(M)
        R_mat = U @ VT
        if np.linalg.det(R_mat) < 0:
            VT[2, :] *= -1
            R_mat = U @ VT
        S_mat = VT.T @ np.diag(sigma) @ VT

        # SLERP on R: convert to quaternion and interpolate
        # SLERP on R: interpolate rotation using quaternions
        key_times = [0, 1]
        key_rots = R.from_matrix([np.eye(3), R_mat])
        slerp = Slerp(key_times, key_rots)
        R_t = slerp(t).as_matrix()

        # Interpolate stretch
        S_t = (1-t) * np.eye(3) + t * S_mat

        # H_t = R_t @ S_t
        M_t = R_t @ S_t
        #*************************************************************************************

        # Apply H_t to each of the 3 gradient vectors (x, y, z coords)
        for coord in range(3):
            A= H_t @ np.linalg.inv(F0)
            B= M_t @ Df0[i]

            G_interp[i, coord] = A @ B[coord]  # (3,)

    return G_interp