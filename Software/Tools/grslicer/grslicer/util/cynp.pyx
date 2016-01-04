import numpy as np

cimport numpy as np
cimport cython

DTYPE = np.float64

ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
def spatial_hash(np.ndarray[DTYPE_t, ndim=1] npmx, DTYPE_t cell_size):
    cdef int a = <int> (npmx[0] // cell_size)
    cdef int b = <int> (npmx[1] // cell_size)
    cdef int c = <int> (npmx[2] // cell_size)
    return ((a * 53) ^ (b * 389) ^ (c * 1543)) % 393241

@cython.boundscheck(False)
def edge_intersection(np.ndarray[DTYPE_t, ndim=1] v1, np.ndarray[DTYPE_t, ndim=1] v2, DTYPE_t height):
    cdef DTYPE_t h1 = v1[2]
    cdef DTYPE_t h2 = v2[2]
    cdef DTYPE_t denominator = h1 - h2
    if denominator == <DTYPE_t> 0.0:
        denominator = <DTYPE_t> 1.0

    cdef DTYPE_t d = (h1 - height) / denominator
    cdef np.ndarray[DTYPE_t, ndim=1] intersection = (1 - d) * v1 + d * v2
    return intersection[:2]
