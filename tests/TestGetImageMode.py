import unittest

from main import get_image_mode


class MyTestCase(unittest.TestCase):
    def test_get_image_mode_rgb(self):
        mode_rgb = "RGB"
        self.assertEqual(get_image_mode("foo.jpg"), mode_rgb)
        self.assertEqual(get_image_mode("foo.jpeg"), mode_rgb)

    def test_get_image_mode_rgba(self):
        self.assertEqual(get_image_mode("foo.png"), "RGBA")


if __name__ == '__main__':
    unittest.main()
