from nltk import RegexpTokenizer, FreqDist
from nltk import SnowballStemmer

from src.data import en_alphabet, STOP, en_swappable_symbols
from src.data import LANG_EN
from src.data import LANG_RU
from src.data import swaps


class TextProcessor:
    REGEXP_TOKENS = r"[a-zA-Zа-яА-Я]+"  # оставляем только слова
    LANG = LANG_RU
    WORD_LEN_TRESHOLD = 2   # Слова меньше 3 символов не учитываем

    def __init__(self, text):
        self.text = text
        self.tokenizer = RegexpTokenizer(self.REGEXP_TOKENS)

    @staticmethod
    def normalize_word(word, preffered_lang=LANG_RU):
        """
        Исправляем орфографию в слове
        :return: Исправленное слово и пришлось ли заменять символы
        """

        def get_language(word):
            if any(w in en_alphabet for w in word):
                # Если есть незаменяемый латинский символ, значит это английское слово
                # Надо будет заменять русские буквы
                return LANG_EN
            if all(w in en_swappable_symbols for w in word): # Например слово TexT
                return preffered_lang
            return LANG_RU

        lang = get_language(word)
        hack = False

        for k, v in swaps[lang].items():
            if k in word:
                word = word.replace(k, v)
                hack = True

        return word, hack

    def set_text(self, text):
        self.text = text
        return self

    @staticmethod
    def lang_detection(tokens, preffered=LANG_RU):
        """
        Пытается определить язык текста по количеству стоп-слов
        В спорных ситуациях предпочтение отдается русскому
        """
        words = [word.lower() for word in tokens]

        language_ratios = {}
        for language in LANG_RU, LANG_EN:
            stopwords_set = STOP[language]
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)
            language_ratios[language] = len(common_elements)

        if language_ratios[LANG_RU] == language_ratios[LANG_EN]:
            return preffered

        return max(language_ratios, key=language_ratios.get)

    def preprocess(self):
        """
        Разбиваем текст на слова
        Пробуем определить язык
        Приводим слова к нормальной форме
        Выделяем корень
        """
        tokens = self.tokenizer.tokenize(self.text)
        lang = TextProcessor.lang_detection(tokens)
        stemmer = SnowballStemmer(lang)

        words = filter(lambda w: len(w) > self.WORD_LEN_TRESHOLD and w not in STOP[lang], tokens)
        words = [TextProcessor.normalize_word(word, preffered_lang=lang) for word in words]

        normalized_words = [word[0].lower() for word in words]
        hack = any(word[1] for word in words)

        return list(map(stemmer.stem, normalized_words)), hack

    def academic_sickness(self):
        """
        Количество повторений топ-5 слов делим на общее количество слов
        """
        words, hack = self.preprocess()
        freq_dist = FreqDist(words)
        top_five = sum([count for _, count in freq_dist.most_common(5)])

        sick = 0
        try:
            sick = top_five / len(words) * 100
        except ZeroDivisionError:
            pass
        return sick, hack