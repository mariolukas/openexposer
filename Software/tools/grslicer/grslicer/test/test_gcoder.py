from unittest import TestCase

from grslicer.gcoder import encode
from grslicer.test import TEST_FILE_CUBE, get_test_settings, get_gcode_filename
from grslicer.importers import import_file
from grslicer.slicer import slice_model


class TestGcoder(TestCase):
    def setUp(self):
        self.s = get_test_settings()
        tm = import_file(TEST_FILE_CUBE, self.s)

        lm = slice_model(tm, self.s)

        self.gcode = get_gcode_filename()
        encode(lm, self.s, self.gcode)

        print 'G-code file:', self.gcode

    def test_gcode(self):
        # TODO: add tests
        print 'testing'
