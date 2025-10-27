import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import sys
import os

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импортируем функцию чтения CSV из нашего вспомогательного модуля
from lib.io_helpers import read_csv

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX с авто-шириной колонок
    """
    # Читаем данные из CSV файла с помощью нашей функции-помощника
    # data - список словарей с данными, fieldnames - список заголовков колонок
    data, fieldnames = read_csv(csv_path)
    
    # Создаем новую рабочую книгу Excel
    wb = Workbook()
    # Получаем активный лист (по умолчанию создается один лист)
    ws = wb.active
    # Устанавливаем название листа
    ws.title = "Sheet1"
    
    # Добавляем заголовки колонок в первую строку Excel
    ws.append(fieldnames)
    
    # Проходим по всем строкам данных и добавляем их в Excel
    for row in data:
        # Для каждой строки создаем список значений в порядке заголовков
        # row.get(field, '') - получаем значение поля или пустую строку если поля нет
        ws.append([row.get(field, '') for field in fieldnames])
    
    # Настраиваем авто-ширину для каждой колонки
    for col_num, column_title in enumerate(fieldnames, 1):  # начинаем с 1, а не с 0
        max_length = 0  # переменная для хранения максимальной длины в колонке
        # Преобразуем номер колонки в буквенное обозначение (1->'A', 2->'B', и т.д.)
        column_letter = get_column_letter(col_num)
        
        # Проверяем длину заголовка колонки
        max_length = max(max_length, len(str(column_title)))
        
        # Проходим по всем строкам данных (начиная со 2-й строки, т.к. 1-я - заголовки)
        for row_num in range(2, ws.max_row + 1):
            # Получаем значение ячейки по координатам (например, 'A2', 'B2', и т.д.)
            cell_value = ws[f"{column_letter}{row_num}"].value
            if cell_value:
                # Обновляем максимальную длину если текущее значение длиннее
                max_length = max(max_length, len(str(cell_value)))
        
        # Вычисляем финальную ширину: максимум из 8 и (макс.длина + 2 пробела)
        adjusted_width = max(8, max_length + 2)
        # Устанавливаем ширину для текущей колонки
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Создаем объект Path для выходного файла
    xlsx_path_obj = Path(xlsx_path)
    # Создаем все необходимые директории если они не существуют
    xlsx_path_obj.parent.mkdir(parents=True, exist_ok=True)
    # Сохраняем рабочую книгу в файл
    wb.save(xlsx_path_obj)

# Блок для прямого запуска файла (тестирование)
if __name__ == "__main__":
    try:
        # Вызываем функцию конвертации с конкретными путями
        csv_to_xlsx("../data/samples/people.csv", "../data/out/people.xlsx")
        print("✓ CSV → XLSX успешно")
        print("Файл создан: src/data/out/people.xlsx")
    except Exception as e:
        # Обрабатываем возможные ошибки и выводим сообщение
        print(f"❌ Ошибка: {e}")