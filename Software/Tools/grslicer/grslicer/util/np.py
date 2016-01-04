from collections import namedtuple

import numpy as np

import grslicer


HASH_NPA = np.array([53, 389, 1543], dtype=np.int32)
HASH_TABLE_SIZE = 393241

Aabb = namedtuple('Aabb', 'min max center')


def vectors_equiv(a, b):
    # Faster than np.array_equiv
    if len(a) is not len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def are_vectors_unique(vectors):
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            if i is not j:
                if vectors_equiv(vectors[i], vectors[j]):
                    return False
    return True


def spatial_hash(npmx, cell_size):
    return ((int(npmx[0] / cell_size) * 53) ^
            (int(npmx[1] / cell_size) * 389) ^
            (int(npmx[2] / cell_size) * 1543)) % 393241


def euclidean_dist(v1, v2):
    return np.linalg.norm(v1 - v2)


def euclidean_dist_square(v1, v2):
    diff = v1 - v2
    return np.dot(diff, diff)


def np_range(start, stop, step, endpoint=True):
    """ Returns an evenly spaced range
    """

    num = ((stop - start) / step) + 1

    return np.linspace(start, stop, num=num, endpoint=endpoint)


def to_ndarray(arr):
    if isinstance(arr, np.ndarray):
        return arr
    return np.array(arr, dtype=grslicer.DEFAULT_COORDINATE_TYPE)


def rotate_xy(mx, theta, center):
    center = center[:2]
    mx = mx - center

    rad = np.radians(theta)
    rotation_mx = np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad), np.cos(rad)]
    ])

    return np.dot(mx, rotation_mx.T) + center


def get_aabb(mx):
    """ Return an Axis-Aligned Bounding Box
    """
    mi = mx.min(axis=0)
    ma = mx.max(axis=0)
    return Aabb(mi, ma, (mi + ma) / 2)


def closest_point_on_edge(v, w, p):
    """ Get closest point to the point p that lies on edge(v,w).
    """
    l2 = euclidean_dist_square(w, v)
    if l2 is 0:
        # edges length is 0
        return v, l2, 0

    t = np.dot(p - v, w - v) / l2
    if t < 0:
        # point is beyond v
        return v, euclidean_dist_square(v, p), 0
    elif t > 1:
        # point is beyond w
        return w, euclidean_dist_square(w, p), 1

    # point is somewhere on the edge, find projection
    projection = v + t * (w - v)
    return projection, euclidean_dist_square(projection, p), 2
