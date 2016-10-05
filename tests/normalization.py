import unittest

from src.textprocessor import TextProcessor


class TestNormalizeWord(unittest.TestCase):

    def test_hack_en(self):
        word = 'wоrd' # о русская
        expected = 'word', True
        actual = TextProcessor.normalize_word(word)
        self.assertEqual(actual, expected, 'Not found english hack')

    def test_hack_ru(self):
        word = 'cлово' # c латинская
        expected = 'слово', True
        actual = TextProcessor.normalize_word(word)
        self.assertEqual(actual, expected, 'Not found russian hack')

    def test_no_hack_ru(self):
        word = 'слово'
        expected = 'слово', False
        actual = TextProcessor.normalize_word(word)
        self.assertEqual(actual, expected, 'Found russian hack')

    def test_no_hack_en(self):
        word = 'sense'
        expected = 'sense', False
        actual = TextProcessor.normalize_word(word)
        self.assertEqual(actual, expected, 'Found english hack')


