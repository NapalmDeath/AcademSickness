from nltk.corpus import stopwords


stop_ru = set(stopwords.words('russian'))
stop_en = set(stopwords.words('english'))

LANG_RU = 'russian'
LANG_EN = 'english'

STOP = {
    LANG_EN: stop_en,
    LANG_RU: stop_ru
}

en2ru = {
    'a': 'а',
    'A': 'А',
    'T': 'Т',
    'y': 'у',
    'o': 'о',
    'O': 'О',
    'K': 'К',
    'p': 'р',
    'P': 'Р',
    'H': 'Н',
    'e': 'е',
    'E': 'Е',
    'M': 'М',
    'c': 'с',
    'C': 'С',
    'x': 'х',
    'X': 'Х',
    'B': 'В'
}
ru2en = dict((v, k) for k, v in en2ru.items())
swaps = {
    LANG_EN: ru2en,
    LANG_RU: en2ru
}

en_swappable_symbols = ''.join(en2ru.keys())
en_alphabet = 'abcdefghijklmnopqrstuvwxyz'
en_alphabet = '{}{}'.format(en_alphabet, en_alphabet.upper())
en_alphabet = set(en_alphabet) - set(en_swappable_symbols)
