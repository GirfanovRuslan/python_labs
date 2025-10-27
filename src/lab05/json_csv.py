import json
import csv
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.io_helpers import read_json, read_csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    """
    data = read_json(json_path)
    
    all_fields = set()
    for item in data:
        all_fields.update(item.keys())
    
    fieldnames = sorted(all_fields)
    
    csv_path_obj = Path(csv_path)
    csv_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    with csv_path_obj.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            row = {field: str(item.get(field, '')) for field in fieldnames}
            writer.writerow(row)

def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей)
    """
    data, fieldnames = read_csv(csv_path)
    
    json_path_obj = Path(json_path)
    json_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    with json_path_obj.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Тест для твоей структуры
    try:
        json_to_csv("../data/samples/people.json", "../data/out/people_from_json.csv")
        print("✓ JSON → CSV успешно")
        
        csv_to_json("../data/samples/people.csv", "../data/out/people_from_csv.json")
        print("✓ CSV → JSON успешно")
        
        print("Файлы созданы в src/data/out/")
    except Exception as e:
        print(f"❌ Ошибка: {e}")