"""
Unit tests for bblab/image/processing.py
Please keep them up-to-date when developing new code.

Run the tests with

>>> python -m unittest

For detailed information please refer to https://readthedocsmissinglink.temp or
docs/source/tests.rst
"""

import os
import unittest
import platform
import numpy
import cv2
from bblab.image import processing
from pathlib import Path

FOLDER_CHANNELS = "./data/1i_channels"
FOLDER_OVERLAY = "./data/1o_overlay"
FOLDER_MASK = "./data/2i_mask"
FOLDER_HIGHLIGHT = "./data/2o_highlight"
FOLDER_MEAN = "./data/3i_mean"
FOLDER_TEMP = "./tests/image"

class TestProcessing(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.expectedFailure
    # also available: @unittest.skip(reason) and @unittest.skipIf(condition, reason)
    def test_check_images_availability(self):
        self.assertEqual(len(os.listdir(Path(FOLDER_CHANNELS))), 3,
                "Channels images not available for tests")
        self.assertEqual(len(os.listdir(Path(FOLDER_OVERLAY))), 1,
                "Overlay image not available for tests")
        # self.assertEqual(len(os.listdir(Path(FOLDER_MASK))), 1,
        #         "Mask image not available for tests")
        # self.assertEqual(len(os.listdir(Path(FOLDER_HIGHLIGHT))), 1,
        #         "Highlight image not available for tests")
        # self.assertEqual(len(os.listdir(Path(FOLDER_MEAN))), 1,
        #         "Mean Csv not available for tests")

    def test_get_filenames_from_folder(self):
        filenames = processing._get_filenames_from_folder(FOLDER_CHANNELS)
        self.assertEqual(len(filenames), 3)

    def test_get_validated_filenames(self):
        filenames = processing._get_filenames_from_folder(FOLDER_CHANNELS)
        self.assertEqual(processing._get_validated_filenames(filenames), filenames)

    # TODO: smarter way to test path...
    def test_build_validated_filename(self):
        filename_function = processing._build_validated_filename(FOLDER_OVERLAY, "fakename", extension=".tiff")
        if platform.system() == "Windows":
            filename_manual = r"data\1o_overlay\fakename.tiff"
        else:
            filename_manual = r"data/1o_overlay/fakename.tiff"
        self.assertEqual(str(filename_function), filename_manual)

    def test_validate_filename(self):
        filename_function = processing._validate_filename(FOLDER_OVERLAY + "/fakename.tiff")
        if platform.system() == "Windows":
            filename_manual = r"data\1o_overlay\fakename.tiff"
        else:
            filename_manual = r"data/1o_overlay/fakename.tiff"
        self.assertEqual(str(filename_function), filename_manual)

    # TODO: using Pillow to load images to be compared? Would it be a double check?
    def test_overlay_channels(self):
        image_processed = processing.overlay_channels(FOLDER_CHANNELS, False, return_image = True)
        files_loaded = processing._get_filenames_from_folder(FOLDER_OVERLAY)
        image_loaded = cv2.imread(str(files_loaded[0]), cv2.IMREAD_UNCHANGED)
        self.assertTrue((image_processed == image_loaded).all())

    @unittest.expectedFailure
    def test_highlight_cells(self):
        self.assertRaises(processing.highlight_cells(), "Update the test, it is a placeholder for a not-already-implemented function")

    @unittest.expectedFailure
    def test_compute_mean(self):
        self.assertRaises(processing.compute_mean(), "Update the test, it is a placeholder for a not-already-implemented function")

# if __name__ == "__main__":
#     unittest.main()