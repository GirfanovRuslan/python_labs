#!/usr/bin/env python3
"""CLI-утилита для работы с текстом - анализ и вывод текстовых файлов"""

import argparse  # Для обработки аргументов командной строки
import sys       # Для системных функций и вывода ошибок
from pathlib import Path  # Для удобной работы с путями файлов

# Добавляем родительскую директорию в путь импорта для поиска модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_text_functions():
    """Получает функции обработки текста из ЛР3 или создаёт резервные реализации"""
    try:
        # Пытаемся импортировать функции из библиотеки text
        from lib.text import normalize, tokenize, count_freq, top_n
        return normalize, tokenize, count_freq, top_n
    except ImportError:
        # Если библиотека не найдена, создаём простые реализации
        import re  # Для регулярных выражений
        
        def normalize(text, *, casefold=True, yo2e=True):
            """Нормализует текст: приводит к нижнему регистру и заменяет ё на е"""
            text = text.casefold() if casefold else text.lower()  # Приводим к нижнему регистру
            return text.replace('ё', 'е') if yo2e else text  # Заменяем ё на е если нужно
        
        # Возвращаем все функции: нормализацию, токенизацию, подсчёт частот и топ-N
        return normalize, \
               lambda t: re.findall(r'\w+(?:-\w+)*', t),  # Токенизатор через регулярки
               lambda t: {w: t.count(w) for w in set(t)},  # Подсчёт частот слов
               lambda f, n: sorted(f.items(), key=lambda x: (-x[1], x[0]))[:n]  # Топ-N слов

def validate_file_path(file_path):
    """Проверка файла с понятными сообщениями об ошибках"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")
    if path.stat().st_size == 0:
        raise ValueError(f"Файл {file_path} пустой")  # Проверяем что файл не пустой
    return path

def read_file(file_path):
    """Чтение файла с полной валидацией и правильной кодировкой"""
    path = validate_file_path(file_path)  # Сначала проверяем файл
    return path.read_text(encoding='utf-8')  # Читаем как текст в UTF-8

def validate_positive_int(value):
    """Валидация положительного целого числа для аргументов"""
    ivalue = int(value)  # Пробуем преобразовать в число
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} должно быть положительным числом")
    return ivalue

def cat_command(args):
    """Команда cat - вывод содержимого файла с нумерацией строк"""
    try:
        # Читаем файл и разбиваем на строки
        lines = read_file(args.input).splitlines()
        
        # Выводим строки с нумерацией или без
        for i, line in enumerate(lines, 1):  # Нумерация с 1
            if args.n:  # Если включена нумерация
                print(f"{i:6d}\t{line}")  # Форматированный вывод с номером строки
            else:
                print(line)  # Простой вывод строки
                
    except (FileNotFoundError, ValueError) as e:
        # Обработка ошибок файлов
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Обработка неожиданных ошибок
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

def stats_command(args):
    """Команда stats - анализ частот слов в тексте"""
    try:
        # Полный pipeline обработки текста:
        # 1. Читаем файл
        # 2. Нормализуем текст (нижний регистр, ё→е)
        # 3. Разбиваем на слова (токенизируем)
        text = read_file(args.input)
        normalized_text = normalize(text)
        tokens = tokenize(normalized_text)
        
        # Проверяем что в тексте есть слова
        if not tokens:
            print("Файл не содержит слов для анализа")
            return
        
        # 4. Подсчитываем частоты слов
        # 5. Выбираем топ-N самых частых слов
        freq = count_freq(tokens)
        
        # Выводим статистику
        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных: {len(freq)}")
        print(f"Топ-{args.top}:")  # Выводим указанное количество топ-слов
        
        # Выводим слова и их частоты
        for word, count in top_n(freq, args.top):
            print(f"  {word}: {count}")
            
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка анализа: {e}", file=sys.stderr)
        sys.exit(1)

# Получаем функции обработки текста один раз при запуске
normalize, tokenize, count_freq, top_n = get_text_functions()

if __name__ == "__main__":
    # Создаём основной парсер аргументов
    parser = argparse.ArgumentParser(
        description="CLI-утилита для работы с текстом",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Создаём подпарсеры для разных команд
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Парсер для команды cat (вывод файла)
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="Путь к входному файлу")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")
    cat_parser.set_defaults(func=cat_command)  # Связываем с функцией cat_command
    
    # Парсер для команды stats (анализ текста)
    stats_parser = subparsers.add_parser("stats", help="Анализ частот слов")
    stats_parser.add_argument("--input", required=True, help="Путь к текстовому файлу")
    stats_parser.add_argument("--top", type=validate_positive_int, default=5, 
                            help="Количество топ-слов (положительное число)")
    stats_parser.set_defaults(func=stats_command)  # Связываем с функцией stats_command
    
    try:
        # Парсим аргументы и выполняем соответствующую команду
        args = parser.parse_args()
        args.func(args)
    except argparse.ArgumentError as e:
        # Обработка ошибок в аргументах командной строки
        print(f"Ошибка аргументов: {e}", file=sys.stderr)
        sys.exit(1)