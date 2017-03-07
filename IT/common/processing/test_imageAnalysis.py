from unittest import TestCase
from common.processing.imageprocessor import ImageAnalysis

class TestImageAnalysis(TestCase):

    def test_enumerate_number_withlines_none(self):
        number = ImageAnalysis.enumerate_number_withlines(False, False, 0)
        self.assertEqual(number, 0)

    def test_enumerate_number_withlines_one(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(False,False,1),1)

    def test_enumerate_number_withlines_two(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(False,False,2),2)

    def test_enumerate_number_withlines_three(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(False,False,3),3)

    def test_enumerate_number_withlines_four(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(True,True,1),4)

    def test_enumerate_number_withlines_five(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(True,True,0),5)

    def test_enumerate_number_withlines_left(self):
        self.assertEqual(ImageAnalysis.enumerate_number_withlines(True,False,0),0)
