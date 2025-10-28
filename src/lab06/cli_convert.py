#!/usr/bin/env python3
"""CLI-утилита для конвертации данных"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def get_convert_functions():
    """Получает функции из ЛР5"""
    try:
        from lab05.json_csv import json_to_csv, csv_to_json
        from lab05.csv_xlsx import csv_to_xlsx
        return json_to_csv, csv_to_json, csv_to_xlsx
    except ImportError:
        import json, csv
        def json_to_csv(j, c):
            with open(j) as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON должен содержать список")
            with open(c, 'w', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        def csv_to_json(c, j):
            with open(c) as f:
                data = list(csv.DictReader(f))
                if not data:
                    raise ValueError("CSV файл не содержит данных")
            with open(j, 'w') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
        
        def csv_to_xlsx(c, x):
            try:
                import openpyxl
            except ImportError:
                raise ImportError("Установите openpyxl: pip install openpyxl")
            wb = openpyxl.Workbook()
            with open(c) as f:
                for i, row in enumerate(csv.reader(f)):
                    for j, val in enumerate(row):
                        wb.active.cell(i+1, j+1, val)
            wb.save(x)
        
        return json_to_csv, csv_to_json, csv_to_xlsx

def validate_file_path(file_path):
    """Проверка файла с понятными ошибками"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")
    return path

def convert_command(args):
    """Общая функция для конвертации"""
    try:
        validate_file_path(args.input)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        converters[args.command](args.input, args.output)
        print(f"Успешно конвертировано: {args.input} -> {args.output}")
    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка данных: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)

# Получаем конвертеры один раз
json_to_csv, csv_to_json, csv_to_xlsx = get_convert_functions()
converters = {'json2csv': json_to_csv, 'csv2json': csv_to_json, 'csv2xlsx': csv_to_xlsx}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI-утилита для конвертации данных",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    for cmd, help_text in [('json2csv', 'Конвертировать JSON в CSV'), 
                          ('csv2json', 'Конвертировать CSV в JSON'), 
                          ('csv2xlsx', 'Конвертировать CSV в XLSX')]:
        p = subparsers.add_parser(cmd, help=help_text)
        p.add_argument("--in", dest="input", required=True, help="Входной файл")
        p.add_argument("--out", dest="output", required=True, help="Выходной файл")
        p.set_defaults(func=convert_command)
    
    try:
        args = parser.parse_args()
        args.func(args)
    except argparse.ArgumentError as e:
        print(f"Ошибка аргументов: {e}", file=sys.stderr)
        sys.exit(1)