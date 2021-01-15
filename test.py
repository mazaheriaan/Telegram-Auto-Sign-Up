import unittest
import utility

class TestUtility(unittest.TestCase):
    def test_word2number(self):
        result = utility.Word2Number("five one one once again your code is one one five one one goodbye")
        self.assertEqual(result,"5 1 1 once again your code is 1 1 5 1 1 goodbye")

if __name__ == '__main__':
    unittest.main()