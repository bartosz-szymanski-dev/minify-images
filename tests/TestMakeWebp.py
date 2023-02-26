import unittest

from PIL import Image
from main import make_webp

import os
import shutil


class TestMakeWebp(unittest.TestCase):
    def test_make_webp(self):
        file_path = "./TestMakeProgressive/public/images/section_big_images/building.png"
        webp_directory = "./TestMakeProgressive/public/images/webp"
        webp_image_path = webp_directory + "/section_big_images/building.webp"
        with Image.open(file_path).convert("RGBA") as img:
            make_webp(file_path, img)
        self.assertTrue(os.path.exists(webp_image_path))
        shutil.rmtree("./TestMakeProgressive/public/images/webp")


if __name__ == '__main__':
    unittest.main()
