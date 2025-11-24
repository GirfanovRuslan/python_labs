#!/usr/bin/env python3
"""CLI-утилита для конвертации данных между форматами JSON, CSV и XLSX"""

import argparse  # Для обработки аргументов командной строки
import sys  # Для работы с системными функциями и stderr
from pathlib import Path  # Для удобной работы с путями файлов

# Добавляем родительскую директорию в путь импорта для поиска модулей lab05
sys.path.insert(0, str(Path(__file__).parent.parent))


def get_convert_functions():
    """Получает функции конвертации из ЛР5 или создаёт резервные реализации"""
    try:
        # Пытаемся импортировать функции из лабораторной работы 5
        from lab05.json_csv import json_to_csv, csv_to_json
        from lab05.csv_xlsx import csv_to_xlsx

        return json_to_csv, csv_to_json, csv_to_xlsx
    except ImportError:
        # Если модули lab05 не найдены, создаём свои реализации
        import json  # Для работы с JSON форматом
        import csv  # Для работы с CSV форматом

        def json_to_csv(j, c):
            """Конвертирует JSON файл в CSV формат"""
            with open(j) as f:
                data = json.load(f)  # Загружаем данные из JSON
                if not isinstance(data, list):
                    raise ValueError("JSON должен содержать список")  # Проверяем формат
            with open(c, "w", newline="") as out:
                # Создаём CSV writer с заголовками из ключей первого элемента
                writer = csv.DictWriter(out, fieldnames=data[0].keys())
                writer.writeheader()  # Записываем заголовок
                writer.writerows(data)  # Записываем все строки данных

        def csv_to_json(c, j):
            """Конвертирует CSV файл в JSON формат"""
            with open(c) as f:
                data = list(csv.DictReader(f))  # Читаем CSV как список словарей
                if not data:
                    raise ValueError(
                        "CSV файл не содержит данных"
                    )  # Проверяем что данные есть
            with open(j, "w") as out:
                # Сохраняем в JSON с красивым форматированием
                json.dump(data, out, ensure_ascii=False, indent=2)

        def csv_to_xlsx(c, x):
            """Конвертирует CSV файл в XLSX формат (Excel)"""
            try:
                import openpyxl  # Библиотека для работы с Excel
            except ImportError:
                raise ImportError("Установите openpyxl: pip install openpyxl")

            wb = openpyxl.Workbook()  # Создаём новую Excel книгу
            with open(c) as f:
                # Читаем CSV построчно и записываем в Excel
                for i, row in enumerate(csv.reader(f)):
                    for j, val in enumerate(row):
                        wb.active.cell(
                            i + 1, j + 1, val
                        )  # Записываем значение в ячейку
            wb.save(x)  # Сохраняем Excel файл

        return json_to_csv, csv_to_json, csv_to_xlsx


def validate_file_path(file_path):
    """Проверка существования файла с понятными сообщениями об ошибках"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")
    return path


def convert_command(args):
    """Общая функция для выполнения конвертации"""
    try:
        # Проверяем что входной файл существует
        validate_file_path(args.input)

        # Создаем директорию для выходного файла если её нет
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)

        # Вызываем соответствующую функцию конвертации
        converters[args.command](args.input, args.output)

        print(f"Успешно конвертировано: {args.input} -> {args.output}")

    except FileNotFoundError as e:
        # Обработка ошибок файлов
        print(f"Ошибка файла: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        # Обработка ошибок данных
        print(f"Ошибка данных: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Обработка всех остальных ошибок
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)


# Получаем функции конвертации один раз при запуске
json_to_csv, csv_to_json, csv_to_xlsx = get_convert_functions()

# Словарь для быстрого доступа к функциям по имени команды
converters = {
    "json2csv": json_to_csv,  # JSON → CSV
    "csv2json": csv_to_json,  # CSV → JSON
    "csv2xlsx": csv_to_xlsx,  # CSV → XLSX
}

if __name__ == "__main__":
    # Создаём основной парсер аргументов
    parser = argparse.ArgumentParser(
        description="CLI-утилита для конвертации данных",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Создаём подпарсеры для разных команд
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Регистрируем все доступные команды конвертации
    for cmd, help_text in [
        ("json2csv", "Конвертировать JSON в CSV"),
        ("csv2json", "Конвертировать CSV в JSON"),
        ("csv2xlsx", "Конвертировать CSV в XLSX"),
    ]:
        # Создаём парсер для каждой команды
        p = subparsers.add_parser(cmd, help=help_text)
        p.add_argument("--in", dest="input", required=True, help="Входной файл")
        p.add_argument("--out", dest="output", required=True, help="Выходной файл")
        p.set_defaults(func=convert_command)  # Связываем с функцией обработки

    try:
        # Парсим аргументы и запускаем соответствующую команду
        args = parser.parse_args()
        args.func(args)
    except argparse.ArgumentError as e:
        # Обработка ошибок в аргументах командной строки
        print(f"Ошибка аргументов: {e}", file=sys.stderr)
        sys.exit(1)
