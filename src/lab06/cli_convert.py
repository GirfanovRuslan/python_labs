#!/usr/bin/env python3
"""
CLI-утилита для конвертации данных между форматами
Использует функции из lab05
"""

import argparse
import sys
from pathlib import Path

def setup_argparse():
    """Настройка парсера аргументов для конвертации"""
    parser = argparse.ArgumentParser(
        description="CLI-утилита для конвертации данных (использует функции из ЛР5)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python cli_convert.py json2csv --in input.json --out output.csv
  python cli_convert.py csv2json --in data.csv --out data.json  
  python cli_convert.py csv2xlsx --in data.csv --out data.xlsx
        """
    )
    
    subparsers = parser.add_subparsers(
        dest="command", 
        help="Доступные команды конвертации",
        required=True,
        metavar="COMMAND"
    )

    # Подкоманда json2csv
    json2csv_parser = subparsers.add_parser("json2csv", help="Конвертировать JSON в CSV")
    json2csv_parser.add_argument(
        "--in", 
        dest="input", 
        required=True,
        type=validate_input_file,
        help="Входной JSON файл"
    )
    json2csv_parser.add_argument(
        "--out", 
        dest="output", 
        required=True,
        type=validate_output_path,
        help="Выходной CSV файл"
    )

    # Подкоманда csv2json
    csv2json_parser = subparsers.add_parser("csv2json", help="Конвертировать CSV в JSON")
    csv2json_parser.add_argument(
        "--in", 
        dest="input", 
        required=True,
        type=validate_input_file,
        help="Входной CSV файл"
    )
    csv2json_parser.add_argument(
        "--out", 
        dest="output", 
        required=True,
        type=validate_output_path,
        help="Выходной JSON файл"
    )

    # Подкоманда csv2xlsx
    csv2xlsx_parser = subparsers.add_parser("csv2xlsx", help="Конвертировать CSV в XLSX")
    csv2xlsx_parser.add_argument(
        "--in", 
        dest="input", 
        required=True,
        type=validate_input_file,
        help="Входной CSV файл"
    )
    csv2xlsx_parser.add_argument(
        "--out", 
        dest="output", 
        required=True,
        type=validate_output_path,
        help="Выходной XLSX файл"
    )

    return parser

def validate_input_file(file_path: str) -> Path:
    """Валидация входного файла"""
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

def validate_output_path(file_path: str) -> Path:
    """Валидация пути для выходного файла"""
    if not file_path or not isinstance(file_path, str):
        raise argparse.ArgumentTypeError("Путь для выходного файла должен быть непустой строкой")
    
    path = Path(file_path)
    
    # Проверяем, что родительская директория существует или может быть создана
    parent_dir = path.parent
    if parent_dir.exists() and not parent_dir.is_dir():
        raise argparse.ArgumentTypeError(f"Родительский путь {parent_dir} не является директорией")
    
    # Проверяем, что файл с таким именем не существует или может быть перезаписан
    if path.exists():
        if not path.is_file():
            raise argparse.ArgumentTypeError(f"{file_path} уже существует и не является файлом")
        try:
            # Проверяем возможность записи
            path.touch()
        except PermissionError:
            raise argparse.ArgumentTypeError(f"Нет прав на запись в файл {file_path}")
        except OSError as e:
            raise argparse.ArgumentTypeError(f"Ошибка доступа к файлу {file_path}: {e}")
    
    # Создаем родительские директории
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    return path

def check_lab5_dependencies():
    """Проверка доступности функций из ЛР5"""
    try:
        from lab05.json_csv import json_to_csv, csv_to_json
        from lab05.csv_xlsx import csv_to_xlsx
        return True
    except ImportError as e:
        print(f"❌ Ошибка: не найдены модули из ЛР5: {e}", file=sys.stderr)
        print("Убедитесь, что функции json_to_csv, csv_to_json, csv_to_xlsx доступны", file=sys.stderr)
        return False

def json_to_csv_cli(args):
    """Конвертация JSON в CSV с использованием функции из ЛР5"""
    if not check_lab5_dependencies():
        sys.exit(1)
    
    from lab05.json_csv import json_to_csv
    
    try:
        json_to_csv(str(args.input), str(args.output))
        print(f"✅ Успешно конвертировано: {args.input} -> {args.output}")
        
    except Exception as e:
        print(f"❌ Ошибка конвертации JSON в CSV: {e}", file=sys.stderr)
        # Удаляем частично созданный файл
        if args.output.exists():
            try:
                args.output.unlink()
                print(f"🗑️  Удален частично созданный файл: {args.output}", file=sys.stderr)
            except:
                pass
        sys.exit(1)

def csv_to_json_cli(args):
    """Конвертация CSV в JSON с использованием функции из ЛР5"""
    if not check_lab5_dependencies():
        sys.exit(1)
    
    from lab05.json_csv import csv_to_json
    
    try:
        csv_to_json(str(args.input), str(args.output))
        print(f"✅ Успешно конвертировано: {args.input} -> {args.output}")
        
    except Exception as e:
        print(f"❌ Ошибка конвертации CSV в JSON: {e}", file=sys.stderr)
        # Удаляем частично созданный файл
        if args.output.exists():
            try:
                args.output.unlink()
                print(f"🗑️  Удален частично созданный файл: {args.output}", file=sys.stderr)
            except:
                pass
        sys.exit(1)

def csv_to_xlsx_cli(args):
    """Конвертация CSV в XLSX с использованием функции из ЛР5"""
    if not check_lab5_dependencies():
        sys.exit(1)
    
    from lab05.csv_xlsx import csv_to_xlsx
    
    try:
        csv_to_xlsx(str(args.input), str(args.output))
        print(f"✅ Успешно конвертировано: {args.input} -> {args.output}")
        
    except Exception as e:
        print(f"❌ Ошибка конвертации CSV в XLSX: {e}", file=sys.stderr)
        # Удаляем частично созданный файл
        if args.output.exists():
            try:
                args.output.unlink()
                print(f"🗑️  Удален частично созданный файл: {args.output}", file=sys.stderr)
            except:
                pass
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
        return

    # Выполняем команду
    if args.command == "json2csv":
        json_to_csv_cli(args)
    elif args.command == "csv2json":
        csv_to_json_cli(args)
    elif args.command == "csv2xlsx":
        csv_to_xlsx_cli(args)
    else:
        print(f"❌ Неизвестная команда: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()