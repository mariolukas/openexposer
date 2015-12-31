from itertools import product

from grslicer.util.np import euclidean_dist_square, to_ndarray, vectors_equiv
from grslicer.util.cynp import spatial_hash


class SpatialHashSimple(object):
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.d = {}

    def add(self, obj):
        cell = spatial_hash(obj.vector, self.cell_size)
        self.d.setdefault(cell, set())
        self.d[cell].add(obj)

    def all_in_cell(self, vector):
        """
            Return all objects in vectors cell
        """
        cell = spatial_hash(vector, self.cell_size)
        return self.d.get(cell)

    def closest_in_cell(self, vector):
        """
            Return the closest object to the passed vector in vectors cell.
        """
        objs = self.all_in_cell(vector)

        if not objs:
            return None

        return min(objs, key=lambda o: euclidean_dist_square(vector, o.vector))

    def find_equal(self, vector):
        """
            Return the object that is represented by the same vector
        """
        objs = self.all_in_cell(vector)

        if not objs:
            return None

        return next((o for o in objs if vectors_equiv(o.vector, vector)), None)


class MergingSpatialHash(SpatialHashSimple):
    def __init__(self, cell_size, dim=3):
        super(MergingSpatialHash, self).__init__(cell_size)
        self.dim = dim
        self.cell_radius = cell_size / 2

        # moves to all neighbor cells
        self._moves = to_ndarray(list(product([0, self.cell_radius, -self.cell_radius], repeat=dim)))

    def add(self, obj):
        for cell in self._neighbour_cells(obj.vector):
            self.d.setdefault(cell, set())
            self.d[cell].add(obj)

    def _neighbour_cells(self, vector):
        moves = vector + self._moves
        return set([spatial_hash(move, self.cell_size) for move in moves])


SpatialHash = SpatialHashSimple