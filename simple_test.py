import sys
import os

# Добавляем src в путь для импорта
sys.path.append('src')

from lab05.json_csv import json_to_csv, csv_to_json
from lab05.csv_xlsx import csv_to_xlsx

def main():
    print("=== ТЕСТ ЛР5 ===")
    
    try:
        # Тест 1: JSON → CSV
        print("1. JSON → CSV...")
        json_to_csv("src/data/lab05/samples/people.json", "src/data/lab05/out/people_from_json.csv")
        print("   ✓ Успешно")
        
        # Тест 2: CSV → JSON  
        print("2. CSV → JSON...")
        csv_to_json("src/data/lab05/samples/people.csv", "src/data/lab05/out/people_from_csv.json")
        print("   ✓ Успешно")
        
        # Тест 3: CSV → XLSX
        print("3. CSV → XLSX...")
        csv_to_xlsx("src/data/lab05/samples/people.csv", "src/data/lab05/out/people.xlsx")
        print("   ✓ Успешно")
        
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("Проверь файлы в: src/data/lab05/out/")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()