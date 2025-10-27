from pathlib import Path
import json
import csv

def read_json(file_path: str) -> list:
    """Чтение JSON файла с проверками"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    if path.stat().st_size == 0:
        raise ValueError(f"Файл {file_path} пустой")
    
    with path.open('r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Файл {file_path} содержит невалидный JSON")
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список")
    
    if len(data) == 0:
        raise ValueError("JSON список пустой")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями")
    
    return data

def read_csv(file_path: str) -> tuple[list, list]:
    """Чтение CSV файла с проверками"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    if path.stat().st_size == 0:
        raise ValueError(f"Файл {file_path} пустой")
    
    with path.open('r', encoding='utf-8') as f:
        sample = f.read(1024)
        f.seek(0)
        
        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)
        except:
            dialect = csv.excel
            has_header = True
        
        if not has_header:
            raise ValueError("CSV файл должен содержать заголовок")
        
        reader = csv.DictReader(f, dialect=dialect)
        rows = list(reader)
    
    if len(rows) == 0:
        raise ValueError("CSV файл не содержит данных")
    
    return rows, reader.fieldnames