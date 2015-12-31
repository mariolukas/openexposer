from unittest import TestCase

from grslicer.importers import import_file
from grslicer.slicer import slice_model
from grslicer.test import TEST_FILE_CUBE, get_test_settings


class TestSlicer(TestCase):
    def setUp(self):
        self.s = get_test_settings()
        tm = import_file(TEST_FILE_CUBE, self.s)

        self.model = slice_model(tm, self.s)
        self.layers = self.model.layers.values()

    def test_skirts(self):
        for layer in self.layers[:2]:
            self.assertEqual(len(layer.skirts), 3)

        for layer in self.layers[2:]:
            self.assertEqual(len(layer.skirts), 0)

    def test_islands(self):
        for layer in self.layers:
            self.assertEqual(len(layer.islands), 1)

    def test_lines(self):
        for layer in self.layers:
            if layer.height <= 3.0:
                # self.assertEqual(len(layer.islands[0].inner_infill), 1)
                pass
            else:
                # self.assertGreaterEqual(len(layer.islands[0].inner_infill), 1)
                pass

    def test_offsets(self):
        for layer in self.layers:
            self.assertEqual(len(layer.islands[0].offsets), 3)
            self.assertEqual(len(layer.islands[0].outer_infill), 2)

            if layer.height <= 3.0:
                for offset in layer.islands[0].offsets:
                    self.assertEqual(len(offset), 1)
            else:
                for offset in layer.islands[0].offsets:
                    self.assertEqual(len(offset), 2)

    def test_slicing_heights(self):
        prev_height = 0.0
        for layer in self.layers:
            self.assertAlmostEqual(prev_height + 0.25, layer.height, places=3)
            prev_height = layer.height
