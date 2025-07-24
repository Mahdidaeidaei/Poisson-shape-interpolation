This repository provides the code for the article with the same name, "Poisson shape interpolation":
https://www.ljll.fr/~frey/papers/morphing/Xu%20D.,%20Poisson%20shape%20interpolation.pdf

The algorithm explained in the article was slightly changed since the original algorithm had some flaws, providing promising results.



Dependencies
Main dependencies that are not included in the repo and should be installed first:

CMake
CUDA (tested with 11.x, 12.x) and cuDNN
Pytorch C++ frontend (tested with 1.7, 1.8, 1.9, 1.10, 2.0)
Vulkan SDK (no mather which version)
Python3
HDF5
