#!/usr/bin/env python3
"""
CLI-утилита для работы с текстом: анализ частот и вывод файлов
Использует функции из lab03 (lib/text.py)
"""

import argparse
import sys
from pathlib import Path

def setup_argparse():
    """Настройка парсера аргументов для текстовых утилит"""
    parser = argparse.ArgumentParser(
        description="CLI-утилита для работы с текстом (использует функции из ЛР3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python cli_text.py cat --input data.txt -n
  python cli_text.py stats --input text.txt --top 10
        """
    )
    
    subparsers = parser.add_subparsers(
        dest="command", 
        help="Доступные команды",
        required=True,
        metavar="COMMAND"
    )

    # Подкоманда cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument(
        "--input", 
        required=True,
        type=validate_file_path,
        help="Путь к входному файлу"
    )
    cat_parser.add_argument(
        "-n", 
        action="store_true", 
        help="Нумеровать строки"
    )

    # Подкоманда stats
    stats_parser = subparsers.add_parser("stats", help="Анализ частот слов в тексте")
    stats_parser.add_argument(
        "--input", 
        required=True,
        type=validate_file_path,
        help="Путь к текстовому файлу"
    )
    stats_parser.add_argument(
        "--top", 
        type=validate_positive_int,
        default=5,
        help="Количество топ-слов (по умолчанию: 5)"
    )

    return parser

def validate_file_path(file_path: str) -> Path:
    """Валидация пути к файлу"""
    if not file_path or not isinstance(file_path, str):
        raise argparse.ArgumentTypeError("Путь к файлу должен быть непустой строкой")
    
    path = Path(file_path)
    
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Файл {file_path} не найден")
    
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{file_path} не является файлом")
    
    try:
        if path.stat().st_size == 0:
            raise argparse.ArgumentTypeError(f"Файл {file_path} пустой")
    except PermissionError:
        raise argparse.ArgumentTypeError(f"Нет доступа к файлу {file_path}")
    except OSError as e:
        raise argparse.ArgumentTypeError(f"Ошибка доступа к файлу {file_path}: {e}")
    
    return path

def validate_positive_int(value: str) -> int:
    """Валидация положительного целого числа"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Должно быть целым числом, получено: {value}")
    
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"Должно быть положительным числом, получено: {value}")
    
    return ivalue

def read_file_safe(file_path: Path, encoding: str = 'utf-8') -> str:
    """Безопасное чтение файла с проверками"""
    try:
        return file_path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        # Пробуем другие распространенные кодировки
        for enc in ['cp1251', 'iso-8859-1', 'utf-16']:
            try:
                return file_path.read_text(encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Не удалось прочитать файл {file_path}. Неподдерживаемая кодировка.")

def cat_command(args):
    """Реализация команды cat"""
    try:
        content = read_file_safe(args.input)
        lines = content.splitlines()
        
        print(f"=== Содержимое файла: {args.input} ===")
        for i, line in enumerate(lines, 1):
            if args.n:
                print(f"{i:6d}\t{line}")
            else:
                print(line)
        print(f"=== Конец файла (строк: {len(lines)}) ===")
                
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)

def stats_command(args):
    """Реализация команды stats с использованием функций из ЛР3"""
    try:
        # Проверяем доступность модулей ЛР3
        try:
            from lib.text import normalize, tokenize, count_freq, top_n
        except ImportError as e:
            raise ImportError(f"Не удалось импортировать функции из ЛР3: {e}")
        
        content = read_file_safe(args.input)
        
        # Используем функции из ЛР3
        normalized_text = normalize(content)
        tokens = tokenize(normalized_text)
        
        if not tokens:
            print("ℹ️  Файл не содержит слов для анализа")
            return
        
        frequencies = count_freq(tokens)
        top_words = top_n(frequencies, args.top)
        
        # Вывод результатов
        print(f"=== Анализ файла: {args.input} ===")
        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных слов: {len(frequencies)}")
        print(f"Топ-{args.top} слов:")
        
        for i, (word, count) in enumerate(top_words, 1):
            print(f"  {i:2d}. {word:<15} : {count:>3}")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе текста: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Основная функция CLI"""
    parser = setup_argparse()
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"❌ Ошибка в аргументах: {e}", file=sys.stderr)
        sys.exit(1)
    except SystemExit:
        # argparse сам выходит при --help, не нужно обрабатывать
        return

    # Выполняем команду
    if args.command == "cat":
        cat_command(args)
    elif args.command == "stats":
        stats_command(args)
    else:
        print(f"❌ Неизвестная команда: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()