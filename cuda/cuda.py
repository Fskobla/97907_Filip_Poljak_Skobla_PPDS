from __future__ import division
from numba import cuda
import numpy
import math
import imageio as iio


@cuda.jit
def my_kernel_3D(io_array):
    x, y, z = cuda.grid(3)
    io_array[x, y, z] = io_array[x, y, z] / 2


data = iio.imread("image.png")
threadsperblock = data.shape
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
blockspergrid_z = math.ceil(data.shape[2] / threadsperblock[2])
blockspergrid = (blockspergrid_x, blockspergrid_y, blockspergrid_z)
my_kernel_3D[blockspergrid, threadsperblock](data)
iio.imwrite("newimage.png", data)
