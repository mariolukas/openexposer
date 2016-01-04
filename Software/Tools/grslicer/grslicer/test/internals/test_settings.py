from unittest import TestCase
import grslicer.settings as gs
from grslicer.test import get_tm_file


class TestSettings(TestCase):

    def test_args(self):
        d = set()
        for group_key, prop in gs.settings_iter():
            self.assertNotIn(prop.arg, d)
            d.add(prop.arg)

    def test_write_read(self):
        s_ref = gs.SlicerSettings()
        for group_key, prop in gs.settings_iter():
            if hasattr(prop, 'low'):
                s_ref[prop.name] = prop.low

            if prop.TYPE is str:
                s_ref[prop.name] = 'asd'

            if prop.TYPE is bool:
                s_ref[prop.name] = not prop.default

        # write to file
        file_name = get_tm_file('.json')
        s_ref.write_file(file_name)

        # read from file
        s_read = gs.SlicerSettings()
        s_read.load_file(file_name)

        # check if the same
        for group_key, prop in gs.settings_iter():
            self.assertEqual(s_ref[prop.name], s_read[prop.name])