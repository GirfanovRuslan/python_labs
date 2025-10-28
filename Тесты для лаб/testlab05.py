import sys
import os

# Добавляем src в путь для импорта
sys.path.append('src')

from lab05.json_csv import json_to_csv, csv_to_json
from lab05.csv_xlsx import csv_to_xlsx

def validate_file_extension(file_path, expected_extensions):
    """Проверяет расширение файла"""
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in expected_extensions:
        expected_str = ", ".join(expected_extensions)
        raise ValueError(f"Ошибка: файл {file_path} должен иметь расширение {expected_str}")

def main():
    print("=== ТЕСТ ЛР5 ===")
    
    try:
        # Тест 1: JSON → CSV
        print("1. JSON → CSV...")
        json_to_csv("data/lab05/samples/people.json", "data/lab05/out/people_from_json.csv")
        print("   ✓ Успешно")
        
        # Тест 2: CSV → JSON  
        print("2. CSV → JSON...")
        validate_file_extension("data/lab05/samples/people.csv", ['.csv'])
        validate_file_extension("data/lab05/out/people_from_csv.json", ['.json'])
        csv_to_json("data/lab05/samples/people.csv", "data/lab05/out/people_from_csv.json")
        print("   ✓ Успешно")
        
        # Тест 3: CSV → XLSX
        print("3. CSV → XLSX...")
        validate_file_extension("data/lab05/samples/people.csv", ['.csv'])
        validate_file_extension("data/lab05/out/people.xlsx", ['.xlsx'])
        csv_to_xlsx("data/lab05/samples/people.csv", "data/lab05/out/people.xlsx")
        print("   ✓ Успешно")
        
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("Проверь файлы в: data/lab05/out/")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()