"""
Unit tests for bblab/image/processing.py
Please keep them up-to-date when developing new code.

Run the tests with

>>> python -m unittest

For detailed information please refer to https://readthedocsmissinglink.temp or
docs/source/tests.rst
"""

import unittest
from bblab.image import processing

class TestProcessing(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.expectedFailure
    # also available: @unittest.skip(reason) and @unittest.skipIf(condition, reason)

    @unittest.expectedFailure
    def test_overlay_channels(self):
        self.assertRaises(processing.overlay_channels(), "Update the test, it is a placeholder for a not-already-implemented function")
    
    @unittest.expectedFailure
    def test_highlight_cells(self):
        self.assertRaises(processing.highlight_cells(), "Update the test, it is a placeholder for a not-already-implemented function")

    @unittest.expectedFailure
    def test_compute_mean(self):
        self.assertRaises(processing.compute_mean(), "Update the test, it is a placeholder for a not-already-implemented function")

# if __name__ == "__main__":
#     unittest.main()