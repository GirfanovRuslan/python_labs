import json
import csv
import os

def validate_input_extension(file_path, expected_ext):
    """Проверяет расширение входного файла"""
    _, ext = os.path.splitext(file_path)
    if ext.lower() != expected_ext.lower():
        raise ValueError(f"Ошибка: входной файл {file_path} должен иметь расширение {expected_ext}")

def validate_output_extension(file_path, expected_ext):
    """Проверяет расширение выходного файла"""
    _, ext = os.path.splitext(file_path)
    if ext.lower() != expected_ext.lower():
        raise ValueError(f"Ошибка: выходной файл {file_path} должен иметь расширение {expected_ext}")

def json_to_csv(json_file, csv_file):
    """Конвертирует JSON в CSV"""
    validate_input_extension(json_file, '.json')
    validate_output_extension(csv_file, '.csv')
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        return
    
    # Если данные - список
    if isinstance(data, list):
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        raise ValueError("JSON должен содержать список объектов")

def csv_to_json(csv_file, json_file):
    """Конвертирует CSV в JSON"""
    validate_input_extension(csv_file, '.csv')
    validate_output_extension(json_file, '.json')
    
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)