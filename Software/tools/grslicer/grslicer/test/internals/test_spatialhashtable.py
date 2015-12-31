from unittest import TestCase

import numpy as np

from grslicer.importers import spatialhashtable
from grslicer.util.np import vectors_equiv
from grslicer import DEFAULT_COORDINATE_TYPE


class Dummy(object):
    def __init__(self, vector):
        self.vector = vector


class TestSimpleSpatialHashTable(TestCase):
    def setUp(self):
        self.table = spatialhashtable.SpatialHashSimple(2.0)
        self.nr = 100
        self.vectors = np.arange(self.nr * 3, dtype=DEFAULT_COORDINATE_TYPE).reshape((self.nr, 3))
        for i in range(self.nr):
            self.table.add(Dummy(self.vectors[i]))

    def test_size(self):
        for i in range(self.nr):
            dummy = self.table.find_equal(self.vectors[i])
            self.assertTrue(vectors_equiv(dummy.vector, self.vectors[i]))