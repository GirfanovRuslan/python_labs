import pytest
from src.lib.text import normalize, tokenize, count_freq, top_n


class TestNormalize:
    # Параметризованный тест - запускает один тест с разными данными
    @pytest.mark.parametrize(
        "source, expected",  # Названия параметров: входные данные и ожидаемый результат
        [
            ("ПрИвЕт\nМИр\t", "привет мир"),  # Тест: верхний регистр + спецсимволы
            ("ёжик, Ёлка", "ежик, елка"),    # Тест: буква ё → е
            ("Hello\r\nWorld", "hello world"), # Тест: английский + переносы строк
            ("  двойные   пробелы  ", "двойные пробелы"), # Тест: лишние пробелы
            ("", ""),                         # Тест: пустая строка (граничный случай)
            ("   ", ""),                      # Тест: только пробелы (граничный случай)
            ("ТЕСТ123test", "тест123test"),   # Тест: цифры + смесь языков
        ]
    )
    def test_normalize(self, source, expected):
        # Проверяем, что normalize(source) возвращает expected
        assert normalize(source) == expected


class TestTokenize:
    @pytest.mark.parametrize(
        "source, expected",
        [
            ("привет мир", ["привет", "мир"]),     # Тест: обычное разделение слов
            ("hello, world!", ["hello", "world"]), # Тест: английский + знаки препинания
            ("один два три", ["один", "два", "три"]), # Тест: несколько слов
            ("", []),                              # Тест: пустая строка
            ("   ", []),                           # Тест: только пробелы
            ("word", ["word"]),                    # Тест: одно слово
        ]
    )
    def test_tokenize(self, source, expected):
        # Проверяем, что tokenize разбивает текст на правильные токены
        assert tokenize(source) == expected


class TestCountFreq:
    def test_basic(self):
        # Тест: подсчет частот в нормальном случае
        tokens = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        result = count_freq(tokens)
        expected = {"apple": 3, "banana": 2, "cherry": 1}
        # Проверяем, что частоты посчитаны правильно
        assert result == expected
    
    def test_empty(self):
        # Тест: пустой список токенов
        assert count_freq([]) == {}  # Должен вернуть пустой словарь
    
    def test_single_word(self):
        # Тест: всего одно слово
        assert count_freq(["test"]) == {"test": 1}  # Должен вернуть {слово: 1}


class TestTopN:
    def test_basic(self):
        # Тест: обычный случай - топ 2 из 4 слов
        freq = {"a": 5, "b": 3, "c": 8, "d": 1}
        result = top_n(freq, 2)
        expected = [("c", 8), ("a", 5)]  # Должен вернуть два самых частых
        assert result == expected
    
    def test_tie_breaker(self):
        # Тест: слова с одинаковой частотой должны сортироваться по алфавиту
        freq = {"z": 3, "a": 3, "m": 3, "b": 2}
        result = top_n(freq, 3)
        # При равной частоте сортировка по алфавиту: a, m, z
        expected = [("a", 3), ("m", 3), ("z", 3)]
        assert result == expected
    
    def test_n_larger_than_dict(self):
        # Тест: запросили больше слов, чем есть в словаре
        freq = {"a": 1, "b": 2}
        result = top_n(freq, 5)
        # Должен вернуть все слова что есть, отсортированные по убыванию частоты
        expected = [("b", 2), ("a", 1)]
        assert result == expected
    
    def test_empty_dict(self):
        # Тест: пустой словарь частот
        assert top_n({}, 5) == []  # Должен вернуть пустой список