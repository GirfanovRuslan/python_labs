from pathlib import Path
import json
import csv


def validate_file_basics(file_path: str) -> Path:
    """Общие проверки файла: существование, доступность и непустота"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        if path.stat().st_size == 0:
            raise ValueError(f"Файл {file_path} пустой")
    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу {file_path}")

    return path


def read_json(file_path: str, encoding: str = "utf-8") -> list:
    """Чтение JSON файла с проверками"""
    path = validate_file_basics(file_path)

    try:
        with path.open("r", encoding=encoding) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Файл {file_path} содержит невалидный JSON: {e}")
    except UnicodeDecodeError:
        raise ValueError(
            f"Неверная кодировка файла {file_path}. Попробуйте другую кодировку."
        )

    # Специфичные для JSON проверки
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список")

    if len(data) == 0:
        raise ValueError("JSON список пустой")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями")

    # Проверка что словари не пустые
    if not all(len(item) > 0 for item in data):
        raise ValueError("Все словари в JSON должны содержать данные")

    return data


def read_csv(file_path: str, encoding: str = "utf-8") -> tuple[list, list]:
    """Чтение CSV файла с проверками"""
    path = validate_file_basics(file_path)

    try:
        with path.open("r", encoding=encoding) as f:
            sample = f.read(1024)
            f.seek(0)

            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
                has_header = sniffer.has_header(sample)
            except csv.Error:
                dialect = csv.excel
                has_header = True

            if not has_header:
                raise ValueError("CSV файл должен содержать заголовок")

            reader = csv.DictReader(f, dialect=dialect)
            rows = list(reader)

            # Проверка целостности данных
            if reader.fieldnames:
                expected_fields = set(reader.fieldnames)
                for i, row in enumerate(rows, 1):
                    if set(row.keys()) != expected_fields:
                        raise ValueError(
                            f"Строка {i} имеет несоответствующее количество полей. Ожидалось: {expected_fields}, получено: {set(row.keys())}"
                        )

    except UnicodeDecodeError:
        raise ValueError(
            f"Неверная кодировка файла {file_path}. Попробуйте другую кодировку."
        )

    if len(rows) == 0:
        raise ValueError("CSV файл не содержит данных")

    # Проверка что есть хотя бы некоторые данные в строках
    if not any(any(row.values()) for row in rows):
        raise ValueError("CSV файл содержит только пустые строки")

    return rows, reader.fieldnames


def validate_extension(file_path: str, expected_ext: str) -> None:
    """Проверка расширения файла"""
    path = Path(file_path)
    ext = path.suffix.lower()
    expected_ext = (
        expected_ext.lower()
        if expected_ext.startswith(".")
        else f".{expected_ext.lower()}"
    )

    if ext != expected_ext:
        raise ValueError(f"Файл {file_path} должен иметь расширение {expected_ext}")


# Дополнительная функция для безопасного создания директорий
def ensure_directory(file_path: str) -> Path:
    """Создает родительские директории если их нет"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
