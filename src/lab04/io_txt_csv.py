# Импорт класса writer из модуля csv для записи данных в CSV формате
from csv import writer

# Импорт модуля для работы с системными параметрами и функциями
import sys

# Импорт модуля для работы с операционной системой (пути, файлы)
import os

# Импорт модуля для современной работы с путями файлов
import pathlib

# Импорт типа Union для аннотаций типов (совместимость с разными версиями Python)
from typing import Union

# Настройка путей импорта: добавляем корневую папку проекта в sys.path
# __file__ - путь к текущему файлу
# os.path.abspath(__file__) - получаем абсолютный путь к файлу
# os.path.dirname() - получаем родительскую директорию пути
# Дважды os.path.dirname() - поднимаемся на 2 уровня вверх по директориям
# sys.path.insert(0, ...) - добавляем этот путь в начало списка поиска модулей Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Определение функции для чтения текстовых файлов
def read_text(path: Union[str, pathlib.Path], encoding: str = "utf-8") -> str:
    """
    Читает весь текст из файла.

    Args:
        path: Путь к файлу (может быть строкой или объектом Path)
        encoding: Кодировка файла (по умолчанию UTF-8)

    Returns:
        Содержимое файла как строка

    Raises:
        FileNotFoundError: Если файл не существует
        UnicodeDecodeError: Если не удается декодировать файл
    """
    # Открываем файл в режиме чтения с указанной кодировкой
    # Конструкция with гарантирует закрытие файла после использования
    with open(path, "r", encoding=encoding) as file:
        # Читаем все содержимое файла в одну строку
        content = file.read()
    # Возвращаем прочитанное содержимое
    return content


# Определение функции для записи данных в CSV файл
def write_csv(
    rows: list[Union[tuple, list]],
    path: Union[str, pathlib.Path],
    header: tuple[str, ...] | None = None,
) -> None:
    """
    Записывает данные в CSV файл.

    Args:
        rows: Список строк данных (каждая строка - кортеж или список)
        path: Путь для сохранения CSV файла
        header: Заголовок колонок (опционально)

    Raises:
        ValueError: Если строки имеют разную длину
        OSError: Если невозможно записать файл
    """
    # Проверка одинаковой длины строк (только если есть данные для записи)
    if rows:
        # Запоминаем длину первой строки как эталон
        first_len = len(rows[0])
        # Перебираем все строки с их индексами
        for i, row in enumerate(rows):
            # Если длина текущей строки не совпадает с эталонной
            if len(row) != first_len:
                # Вызываем ошибку с информацией о проблемной строке
                raise ValueError(
                    f"Строка {i} имеет длину {len(row)}, ожидалось {first_len}"
                )

    # Создание родительских директорий если их нет
    # Path(path) - создаем объект Path из переданного пути
    # .parent - получаем родительскую директорию
    # .mkdir() - создаем директорию
    # parents=True - создаем все промежуточные директории
    # exist_ok=True - не вызываем ошибку если директория уже существует
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Открываем файл для записи в CSV формате
    # 'w' - режим записи (перезапись файла)
    # newline="" - правильная обработка переносов строк для CSV
    # encoding="utf-8" - записываем в кодировке UTF-8
    with open(path, "w", newline="", encoding="utf-8") as file:
        # Создаем объект writer для записи CSV данных
        w = writer(file)
        # Если передан заголовок (не None)
        if header is not None:
            # Записываем одну строку заголовка
            # writerow() - для записи одной строки
            w.writerow(header)
        # Записываем все строки данных
        # writerows() - для записи нескольких строк
        w.writerows(rows)
