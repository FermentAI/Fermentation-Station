import unittest
import rms
from rms import main2
import os

class Testfiles(unittest.TestCase):

    def test_display_page1(self):
        tester_path = '/'
        isExist = os.path.exists(main2.display_page(tester_path)
        self.assertTrue(isExist)
    def test_display_page2(self):
        tester_path = '/'
        isFile = os.path.isfile(main2.display_page(tester_path))
        self.assertTrue(isFile)
