import unittest

from main import create_directory

import os
import shutil


class TestCreateDirectory(unittest.TestCase):
    def test_create_foo_bar_directory(self):
        test_root_directory = './path'
        directory_path = test_root_directory + "/to/directory"
        file_name = "file.jpg"
        full_path = directory_path + "/" + file_name
        create_directory(full_path)
        self.assertTrue(os.path.exists(directory_path))
        self.assertTrue(os.path.isdir(directory_path))
        shutil.rmtree(test_root_directory)


if __name__ == '__main__':
    unittest.main()
