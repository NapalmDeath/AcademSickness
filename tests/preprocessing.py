import unittest

from src.data import LANG_RU, LANG_EN
from src.textprocessor import TextProcessor


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessor('')

    def test_happy_scenario(self):
        text = 'Девушка взяла женский спортивный костюм в женскую раздевалку.'
        expected = ['девушк', 'взял', 'женск', 'спортивн', 'костюм', 'женск', 'раздевалк']
        actual = self.text_processor.set_text(text).preprocess()[0]
        self.assertEqual(actual, expected, 'Incorrect preprocessing')

    def test_dirty_text(self):
        text = '$#%@ soMe     $^%&*& @#$ dIrty TexT )))=)'
        expected = ['some', 'dirti', 'text']
        actual = self.text_processor.set_text(text).preprocess()[0]
        self.assertEqual(actual, expected, 'Incorrect preprocessing')

    def test_lang_detection_ru(self):
        text = ['Бытовки', 'в', 'наличии', 'и', 'на', 'заказ']
        expected = LANG_RU
        actual = TextProcessor.lang_detection(text)
        self.assertEqual(actual, expected, 'Error in lang detection')

    def test_lang_detection_en(self):
        text = ['Some', 'english', 'text', 'with', 'stop', 'words']
        expected = LANG_EN
        actual = TextProcessor.lang_detection(text)
        self.assertEqual(actual, expected, 'Error in lang detection')