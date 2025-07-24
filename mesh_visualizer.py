import numpy as np
import pyvista as pv

def visualize_mesh():

    mesh = pv.read(f"samples/result_mesh_melange.ply")

    # Plot the mesh with better details
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color='lightblue', show_edges=True, opacity=1.0)

    # Set the background color to white
    plotter.set_background('white')

    # Show the interactive plot
    plotter.show()