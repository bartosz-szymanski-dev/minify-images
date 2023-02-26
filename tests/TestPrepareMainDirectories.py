import unittest

from main import prepare_main_directories

import os
import shutil


def clean_up_directories():
    if os.path.exists("./public"):
        shutil.rmtree("./public")


class MyTestCase(unittest.TestCase):
    def test_prepare_main_directories(self):
        clean_up_directories()

        prepare_main_directories()
        for directory in ["progressive", "webp"]:
            self.assertTrue(os.path.exists("./public/images/" + directory))

        clean_up_directories()


if __name__ == '__main__':
    unittest.main()
