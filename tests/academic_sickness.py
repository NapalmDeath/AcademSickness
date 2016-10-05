import unittest

from src.textprocessor import TextProcessor


class TestAcademicSickness(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessor('')

    def test_empty_text(self):
        expected = 0, False
        actual = self.text_processor.academic_sickness()
        self.assertEqual(actual, expected, 'Incorrect sickness for empty text')

    def test_happy_scenario(self):
        text = 'abc def ghk qwe ewq ytr yui abc'
        expected = 75
        actual = self.text_processor.set_text(text).academic_sickness()[0]
        self.assertEqual(actual, expected, 'Incorrect sickness')

    def test_all_equal_words(self):
        text = 'abc abc'
        expected = 100
        actual = self.text_processor.set_text(text).academic_sickness()[0]
        self.assertEqual(actual, expected, 'Incorrect sickness for full equal text')