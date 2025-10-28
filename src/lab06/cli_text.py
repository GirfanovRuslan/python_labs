#!/usr/bin/env python3
"""CLI-утилита для работы с текстом"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def get_text_functions():
    """Получает функции из ЛР3"""
    try:
        from lib.text import normalize, tokenize, count_freq, top_n
        return normalize, tokenize, count_freq, top_n
    except ImportError:
        import re
        def normalize(text, *, casefold=True, yo2e=True):
            text = text.casefold() if casefold else text.lower()
            return text.replace('ё', 'е') if yo2e else text
        return normalize, lambda t: re.findall(r'\w+(?:-\w+)*', t), \
               lambda t: {w: t.count(w) for w in set(t)}, \
               lambda f, n: sorted(f.items(), key=lambda x: (-x[1], x[0]))[:n]

def validate_file_path(file_path):
    """Проверка файла с понятными ошибками"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")
    if path.stat().st_size == 0:
        raise ValueError(f"Файл {file_path} пустой")
    return path

def read_file(file_path):
    """Чтение файла с полной валидацией"""
    path = validate_file_path(file_path)
    return path.read_text(encoding='utf-8')

def validate_positive_int(value):
    """Валидация положительного числа"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} должно быть положительным числом")
    return ivalue

def cat_command(args):
    """Вывод содержимого файла"""
    try:
        lines = read_file(args.input).splitlines()
        for i, line in enumerate(lines, 1):
            print(f"{i:6d}\t{line}" if args.n else line)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

def stats_command(args):
    """Анализ частот слов"""
    try:
        tokens = tokenize(normalize(read_file(args.input)))
        if not tokens:
            print("Файл не содержит слов для анализа")
            return
        
        freq = count_freq(tokens)
        print(f"Всего слов: {len(tokens)}\nУникальных: {len(freq)}\nТоп-{args.top}:")
        for word, count in top_n(freq, args.top):
            print(f"  {word}: {count}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка анализа: {e}", file=sys.stderr)
        sys.exit(1)

# Получаем функции один раз
normalize, tokenize, count_freq, top_n = get_text_functions()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI-утилита для работы с текстом",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="Путь к входному файлу")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")
    cat_parser.set_defaults(func=cat_command)
    
    stats_parser = subparsers.add_parser("stats", help="Анализ частот слов")
    stats_parser.add_argument("--input", required=True, help="Путь к текстовому файлу")
    stats_parser.add_argument("--top", type=validate_positive_int, default=5, 
                            help="Количество топ-слов (положительное число)")
    stats_parser.set_defaults(func=stats_command)
    
    try:
        args = parser.parse_args()
        args.func(args)
    except argparse.ArgumentError as e:
        print(f"Ошибка аргументов: {e}", file=sys.stderr)
        sys.exit(1)