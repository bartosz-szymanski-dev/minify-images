import unittest

from main import inject_optimized_directory_into_path


class TestInjectOptimizedDirectoryIntoPath(unittest.TestCase):

    def test_inject_progressive_directory(self):
        output = inject_optimized_directory_into_path("progressive", "./public/images/some-directory/file.jpg")
        expected_result = "./public/images/progressive/some-directory/file.jpg"
        self.assertEqual(output, expected_result)

    def test_inject_webp_directory(self):
        output = inject_optimized_directory_into_path("webp", "./public/images/some-directory/file.png")
        expected_result = "./public/images/webp/some-directory/file.png"
        self.assertEqual(output, expected_result)


if __name__ == '__main__':
    unittest.main()
