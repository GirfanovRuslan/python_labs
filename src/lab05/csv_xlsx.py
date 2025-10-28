import csv
import openpyxl
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

def csv_to_xlsx(csv_file, xlsx_file):
    """Конвертирует CSV в XLSX используя openpyxl"""
    validate_input_extension(csv_file, '.csv')
    validate_output_extension(xlsx_file, '.xlsx')
    
    # Создаем новую книгу Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    # Читаем CSV и записываем в XLSX
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader, 1):
            for col_idx, value in enumerate(row, 1):
                sheet.cell(row=row_idx, column=col_idx, value=value)
    
    # Сохраняем файл
    workbook.save(xlsx_file)