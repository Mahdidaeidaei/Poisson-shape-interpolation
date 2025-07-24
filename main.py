import numpy as np
import trimesh
import argparse


from mesh_loader import load_ply_vertices_faces
from gradient_field_calculator import compute_gradient_field_with_normals
from divergence_calculator import compute_divergence
from laplacian_calculator import cotangent_laplacian
from poisson_solver import solve_poisson_with_constraint
from interpolator import nonlinear_gradient_interpolation
from mesh_visualizer import visualize_mesh



# === Main usage ===
def mixer_fun(index_i, index_j , t):
    
    V0, F0 = load_ply_vertices_faces(f"samples/{index_i}.ply")
    V1, F1 = load_ply_vertices_faces(f"samples/{index_j}.ply")

    assert np.all(F0 == F1), "Meshes must share the same connectivity!"

    _ , Df0 = compute_gradient_field_with_normals(V0, F0)  # Shape (n_faces, 3, 3)
    #print("G0 shape:", G0.shape)
    _ , Df1 = compute_gradient_field_with_normals(V1, F1)


    #t= 0.5 #t=1 problematic
    # Interpolated G example (linear interpolation at t = 0.5)
    G_interp = nonlinear_gradient_interpolation(Df0, Df1, V0, V1, F0, t=t)
    #G_interp = (1-t) * G0 + t * G1

    V05 = (1-t) * V0 + t * V1

    #print(V0.shape, F0.shape)
    L = cotangent_laplacian(V05, F0)
    #rank = np.linalg.matrix_rank(L.toarray())
    #print(f"Rank of Laplacian: {rank} / {L.shape[0]}")

    V_interp = np.zeros_like(V05)

    for i in range(3):  # x, y, z
        b = compute_divergence(V05, F0,  G_interp[:, i, :])
        V_interp[:, i] = solve_poisson_with_constraint(L, b, fixed_index=0, fixed_value= (1-t) * V0[0, i] + t * V1[0, i])


    # Save to ply file
    mesh_interp = trimesh.Trimesh(vertices=V_interp, faces=F0, process=True)
    mesh_interp.export('samples/result_mesh_melange.ply')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mix two PLY meshes")
    parser.add_argument("index_i", type=str, help="First mesh name (without extension)")
    parser.add_argument("index_j", type=str, help="Second mesh name (without extension)")
    parser.add_argument("--t", type=float, default=0.5, help="Interpolation factor (default: 0.5)")

    args = parser.parse_args()

    mixer_fun(args.index_i, args.index_j, t=args.t)

    # Visualize the result
    visualize_mesh()



