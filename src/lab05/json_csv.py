import json
import csv
import os
from pathlib import Path

def validate_file_exists(file_path: str) -> Path:
    """Проверяет существование файла и возвращает Path объект"""
    if not file_path or not isinstance(file_path, str):
        raise ValueError("Путь к файлу должен быть непустой строкой")
    
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")
    
    return path

def validate_file_not_empty(path: Path) -> None:
    """Проверяет что файл не пустой"""
    try:
        if path.stat().st_size == 0:
            raise ValueError(f"Файл {path} пустой")
    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу {path}")
    except OSError as e:
        raise OSError(f"Ошибка доступа к файлу {path}: {e}")

def validate_input_extension(file_path: str, expected_ext: str) -> None:
    """Проверяет расширение входного файла"""
    if not expected_ext.startswith('.'):
        expected_ext = '.' + expected_ext
    
    path = validate_file_exists(file_path)
    validate_file_not_empty(path)
    
    ext = path.suffix.lower()
    expected_ext = expected_ext.lower()
    
    if ext != expected_ext:
        raise ValueError(f"Ошибка: входной файл {file_path} должен иметь расширение {expected_ext}")

def validate_output_extension(file_path: str, expected_ext: str) -> None:
    """Проверяет расширение выходного файла"""
    if not expected_ext.startswith('.'):
        expected_ext = '.' + expected_ext
    
    if not file_path or not isinstance(file_path, str):
        raise ValueError("Путь к файлу должен быть непустой строкой")
    
    path = Path(file_path)
    ext = path.suffix.lower()
    expected_ext = expected_ext.lower()
    
    if ext != expected_ext:
        raise ValueError(f"Ошибка: выходной файл {file_path} должен иметь расширение {expected_ext}")
    
    # Создаем директорию если её нет
    path.parent.mkdir(parents=True, exist_ok=True)

def validate_json_structure(data) -> None:
    """Проверяет структуру JSON данных"""
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список объектов")
    
    if len(data) == 0:
        raise ValueError("JSON список пустой")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями")
    
    # Проверяем что все словари имеют одинаковые ключи
    if len(data) > 1:
        first_keys = set(data[0].keys())
        for i, item in enumerate(data[1:], 1):
            if set(item.keys()) != first_keys:
                raise ValueError(f"Элемент {i} имеет несовпадающие ключи с первым элементом")

def json_to_csv(json_file: str, csv_file: str, encoding: str = 'utf-8') -> None:
    """Конвертирует JSON в CSV"""
    validate_input_extension(json_file, '.json')
    validate_output_extension(csv_file, '.csv')
    
    try:
        # Чтение JSON с проверкой кодировки
        with open(json_file, 'r', encoding=encoding) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Файл {json_file} содержит невалидный JSON: {e}")
    except UnicodeDecodeError:
        raise ValueError(f"Неверная кодировка файла {json_file}. Попробуйте другую кодировку.")
    
    # Проверка структуры данных
    validate_json_structure(data)
    
    # Запись CSV
    try:
        with open(csv_file, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        # Удаляем частично записанный файл при ошибке
        if os.path.exists(csv_file):
            os.remove(csv_file)
        raise Exception(f"Ошибка записи CSV файла: {e}")

def csv_to_json(csv_file: str, json_file: str, encoding: str = 'utf-8') -> None:
    """Конвертирует CSV в JSON"""
    validate_input_extension(csv_file, '.csv')
    validate_output_extension(json_file, '.json')
    
    data = []
    try:
        # Чтение CSV
        with open(csv_file, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            
            # Проверяем что CSV имеет заголовки
            if not reader.fieldnames:
                raise ValueError("CSV файл не содержит заголовков")
            
            # Проверяем что все строки имеют одинаковое количество полей
            expected_fields = set(reader.fieldnames)
            for i, row in enumerate(reader, 1):
                if set(row.keys()) != expected_fields:
                    raise ValueError(f"Строка {i} имеет несоответствующее количество полей")
                data.append(row)
                
    except UnicodeDecodeError:
        raise ValueError(f"Неверная кодировка файла {csv_file}. Попробуйте другую кодировку.")
    
    if len(data) == 0:
        raise ValueError("CSV файл не содержит данных")
    
    # Запись JSON
    try:
        with open(json_file, 'w', encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Удаляем частично записанный файл при ошибке
        if os.path.exists(json_file):
            os.remove(json_file)
        raise Exception(f"Ошибка записи JSON файла: {e}")