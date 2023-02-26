import unittest

from PIL import Image

from main import make_progressive

import os
import shutil


class TestMakeProgressive(unittest.TestCase):
    def test_make_progressive_big(self):
        self.abstract_progressive_test("/section_big_images/building.png", 168, 77)

    def test_make_progressive_small(self):
        self.abstract_progressive_test("/favicon-16x16.png", 1, 1)

    def abstract_progressive_test(self, path_to_file_after_images, desired_width, desired_height):
        file_path = "./TestMakeProgressive/public/images" + path_to_file_after_images
        progressive_directory = "./TestMakeProgressive/public/images/progressive"
        progressive_image_path = progressive_directory + path_to_file_after_images
        with Image.open(file_path).convert("RGBA") as img:
            make_progressive(file_path, img)
        self.assertTrue(os.path.exists(progressive_image_path))
        with Image.open(progressive_image_path) as created_img:
            width, height = created_img.size
            self.assertEqual(desired_width, width)
            self.assertEqual(desired_height, height)
        shutil.rmtree("./TestMakeProgressive/public/images/progressive")


if __name__ == '__main__':
    unittest.main()
