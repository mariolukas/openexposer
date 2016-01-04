from unittest import TestCase

import numpy as np

from grslicer.importers import import_file
from grslicer.importers.stl import StlBinImporter, StlAsciiImporter
from grslicer.model import TopoModel
from grslicer.test import TEST_FILES, get_test_settings


class TestImporter(TestCase):
    def setUp(self):
        self.settings = get_test_settings()

    def test_import(self):
        for file_path, desc in TEST_FILES.items():
            self.can_import(file_path, desc)

    def can_import(self, file_path, desc):
        with open(file_path) as f:
            contents = f.read()
            if desc['type'] is 'bin':
                self.assertTrue(StlBinImporter.can_import(contents))
                self.assertFalse(StlAsciiImporter.can_import(contents))
            elif desc['type'] is 'ascii':
                self.assertFalse(StlBinImporter.can_import(contents))
                self.assertTrue(StlAsciiImporter.can_import(contents))
            else:
                self.fail('Importer not supported')

            result = import_file(file_path, self.settings)
            check_result(self, result, desc)


def check_result(test_case, result, result_data):
    test_case.assertIsInstance(result, TopoModel)
    test_case.assertEqual(len(result.vertices), result_data['nr_vertices'])
    test_case.assertEqual(len(result.faces), result_data['nr_faces'])
    test_case.assertEqual(result.mx.shape, (result_data['nr_vertices'], 3))

    aabb = result.aabb
    test_case.assertAlmostEqual(aabb.min[2], 0, places=5)

    if 'nr_edges' in result_data:
        test_case.assertEqual(len(result.edges), result_data['nr_edges'])

    if 'euler' in result_data:
        test_case.assertEqual(result.get_euler(), result_data['euler'])

    if 'aabb' in result_data:

        test_case.assertTrue(np.array_equal(result_data['aabb'], aabb.max - aabb.min))
