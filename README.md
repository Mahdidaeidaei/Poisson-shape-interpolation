# Poisson Shape Interpolation
This repository provides the code for the article with the same name, **Poisson shape interpolation**:
https://www.ljll.fr/~frey/papers/morphing/Xu%20D.,%20Poisson%20shape%20interpolation.pdf

The algorithm explained in the article was slightly changed since the original algorithm had some flaws, providing promising results.



# Dependencies
Main dependencies that are not included in the repo and should be installed first (with PIP or conda):

trimesh   
pyvista

# Instructions

The code takes two triangular surface meshes that must be compatible. Compatible meshes share the same node and mesh connectivity. For more information, please feel free to revisit the article.  

Two compatible meshes must be put in the **samples** folder in *ply* format. I have already provided two samples:
**cube_projected.ply**  and **sphere_projected.ply**

Two samples are a cube and a sphere mesh, and the expected result shape must be a shape between:

<img width="788" height="751" alt="image" src="https://github.com/user-attachments/assets/b401d677-3eac-4495-8cef-015b1f76c4fb" />        

*the cube*

      
<img width="773" height="720" alt="image" src="https://github.com/user-attachments/assets/42b21381-7e12-4247-8c19-9c07fc2927e4" />    

*the sphere*  


<img width="799" height="726" alt="image" src="https://github.com/user-attachments/assets/87a96d52-01ed-43a5-8a2e-4bf21397e0fd" />

*interpolated shape*





After installing the libraries in your environment, launch this line in a command prompt (in case of using Anaconda paste it in the anaconda prompt while your environment is activated):

```
python main.py sphere_projected cube_projected --t 0.5
```

The first two arguments are the names of the input meshes, and the last argument is the transition parameter (0 means the interpolated shape will be the first mesh, 1 means the second mesh, for getting something in between, put 0.5)








