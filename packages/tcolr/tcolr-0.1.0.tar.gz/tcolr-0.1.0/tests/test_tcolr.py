from io import StringIO
import unittest
from unittest.mock import patch
import os

from tcolr import TColr


def fixture(type, name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', type, name)

def expected(expected):
    fixture_file = fixture('expected', expected)
    with open(fixture_file, 'r') as f:
        expected_output = f.read()
    return expected_output


class TestTColr(unittest.TestCase):
    def setUp(self):
        self.arguments = {
            'log_level': 'error',
            'config': 'config.yaml',
            'input': 'input.txt'
        }
        self.tcolr = TColr(self.arguments)
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_tcolr_output(self, mock_stdout):
        self.tcolr.run({'input': fixture('inputs', 'test-output.yaml')})
        output = mock_stdout.getvalue()
        self.assertEqual(output, expected('test-output.yaml'))

if __name__ == '__main__':
    unittest.main()