"""
Copyright 2022 Filip Poljak Skobla. All Rights Reserved.
Licensed to GPLv2 www.gnu.org/licenses/old-licenses/gpl-2.0.html
Image process with CUDA
"""

from __future__ import division
from numba import cuda
import numpy
import math
import imageio as iio


@cuda.jit
def my_kernel_3D(io_array):
    """
        Function of kernel with 3D grid (representing image)
    """
    x, y, z = cuda.grid(3)
    # Current image reduce lightness by half
    io_array[x, y, z] = io_array[x, y, z] / 2

# Read random image
data = iio.imread("image.png")
threadsperblock = data.shape
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
blockspergrid_z = math.ceil(data.shape[2] / threadsperblock[2])
blockspergrid = (blockspergrid_x, blockspergrid_y, blockspergrid_z)
my_kernel_3D[blockspergrid, threadsperblock](data)
# Write into file the modified image
iio.imwrite("newimage.png", data)
