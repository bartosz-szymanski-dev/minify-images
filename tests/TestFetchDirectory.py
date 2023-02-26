import unittest

from main import fetch_directory
import os
import shutil


class TestFetchDirectory(unittest.TestCase):
    def test_fetch_directory(self):
        fetch_directory("./TestFetchDirectory/public/images")
        self.assertTrue(os.path.exists("./public/images/shapes/triangle-faded.png"))
        shutil.rmtree("./public")


if __name__ == '__main__':
    unittest.main()
