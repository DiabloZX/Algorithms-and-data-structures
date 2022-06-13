import unittest
from fuzzy_search import find_substring_cords


class MyTestCase(unittest.TestCase):
    def test_1(self):
        result = find_substring_cords("hello helllo hellllo", "hello", 0)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (0, 5))

    def test_2(self):
        result = find_substring_cords("hello", "hello", 1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (0, 4))
        self.assertEqual(result[1], (0, 5))

    def test_3(self):
        result = find_substring_cords("hello", "hello", 2)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (0, 3))
        self.assertEqual(result[1], (0, 4))
        self.assertEqual(result[2], (0, 5))

    def test_4(self):
        result = find_substring_cords("henlo", "hello", 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (0, 5))

    def test_5(self):
        result = find_substring_cords("helo ", "hello", 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (0, 4))


if __name__ == '__main__':
    unittest.main()
