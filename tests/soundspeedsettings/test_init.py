from __future__ import absolute_import, division, print_function, unicode_literals

import unittest


class TestSoundSpeedSettingsInit(unittest.TestCase):

    def test_has_version(self):
        from hyo.soundspeedsettings import __version__
        self.assertIsNot(len(__version__), 0)

    def test_is_version_more_than_3(self):
        from hyo.soundspeedsettings import __version__
        self.assertGreaterEqual(int(__version__.split('.')[0]), 3)

    def test_doc(self):
        from hyo.soundspeedsettings import __doc__
        self.assertIsNot(len(__doc__), 0)

    def test_is_sound_in_doc(self):
        from hyo.soundspeedsettings import __doc__
        self.assertTrue("sound" in __doc__.lower(), 0)

    def test_author(self):
        from hyo.soundspeedsettings import __author__
        self.assertIsNot(len(__author__), 0)

    def test_has_multiple_authors(self):
        from hyo.soundspeedsettings import __author__
        self.assertGreater(len(__author__.split(';')), 0)

    def test_license(self):
        from hyo.soundspeedsettings import __license__
        self.assertIsNot(len(__license__), 0)

    def test_has_lgpl_in_license(self):
        from hyo.soundspeedsettings import __license__
        self.assertTrue("lgpl" in __license__.lower())

    def test_copyright(self):
        from hyo.soundspeedsettings import __copyright__
        self.assertIsNot(len(__copyright__), 0)

    def test_has_current_year_in_copyright(self):
        from hyo.soundspeedsettings import __copyright__
        from datetime import datetime
        self.assertTrue((("%s" % datetime.now().year) in __copyright__) or
                        (("%s" % (datetime.now().year + 1)) in __copyright__))


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSoundSpeedSettingsInit))
    return s
