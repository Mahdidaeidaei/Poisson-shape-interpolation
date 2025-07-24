import numpy as np
import trimesh

def load_ply_vertices_faces(path):
    mesh = trimesh.load(path, process=False)
    V = mesh.vertices
    F = mesh.faces
    return V, F