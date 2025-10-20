from csv import writer
import sys
import os
import pathlib
from typing import Union

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def read_text(path: Union[str, pathlib.Path], encoding: str = "utf-8") -> str:
    """
    Читает весь текст из файла.
    
    Args:
        path: Путь к файлу
        encoding: Кодировка файла
        
    Returns:
        Содержимое файла как строка
        
    Raises:
        FileNotFoundError: Если файл не существует
        UnicodeDecodeError: Если не удается декодировать файл
    """
    with open(path, 'r', encoding=encoding) as file:
        content = file.read()
    return content

def write_csv(rows: list[Union[tuple, list]], path: Union[str, pathlib.Path], 
              header: tuple[str, ...] | None = None) -> None:
    """
    Записывает данные в CSV файл.
    
    Args:
        rows: Список строк данных
        path: Путь для сохранения CSV файла
        header: Заголовок колонок
        
    Raises:
        ValueError: Если строки имеют разную длину
        OSError: Если невозможно записать файл
    """
    # Проверка одинаковой длины строк
    if rows:
        first_len = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != first_len:
                raise ValueError(f"Строка {i} имеет длину {len(row)}, ожидалось {first_len}")
    
    # Создание родительских директорий
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', newline="", encoding="utf-8") as file:
        w = writer(file)
        if header is not None:
            w.writerow(header)  # writerow (единственное число) для заголовка
        w.writerows(rows)       # writerows (множественное число) для данных