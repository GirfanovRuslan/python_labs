import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.io_helpers import read_csv

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX с авто-шириной колонок
    """
    data, fieldnames = read_csv(csv_path)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    ws.append(fieldnames)
    
    for row in data:
        ws.append([row.get(field, '') for field in fieldnames])
    
    for col_num, column_title in enumerate(fieldnames, 1):
        max_length = 0
        column_letter = get_column_letter(col_num)
        
        max_length = max(max_length, len(str(column_title)))
        
        for row_num in range(2, ws.max_row + 1):
            cell_value = ws[f"{column_letter}{row_num}"].value
            if cell_value:
                max_length = max(max_length, len(str(cell_value)))
        
        adjusted_width = max(8, max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    xlsx_path_obj = Path(xlsx_path)
    xlsx_path_obj.parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path_obj)

if __name__ == "__main__":
    try:
        csv_to_xlsx("../data/samples/people.csv", "../data/out/people.xlsx")
        print("✓ CSV → XLSX успешно")
        print("Файл создан: src/data/out/people.xlsx")
    except Exception as e:
        print(f"❌ Ошибка: {e}")