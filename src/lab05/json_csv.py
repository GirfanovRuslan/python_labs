# Импорт необходимых модулей
import json  # Для работы с JSON форматом
import csv   # Для работы с CSV форматом
from pathlib import Path  # Для работы с путями файлов
import sys    # Для работы с системными параметрами
import os     # Для работы с операционной системой

# Добавляем родительскую директорию в путь Python для импорта наших модулей
# Это нужно чтобы можно было импортировать модули из папки lib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импортируем наши вспомогательные функции для чтения файлов
from lib.io_helpers import read_json, read_csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV формат.
    Принимает путь к JSON файлу и путь для сохранения CSV файла.
    """
    # Читаем данные из JSON файла с помощью нашей функции-помощника
    # Функция read_json возвращает список словарей
    data = read_json(json_path)
    
    # Создаем пустое множество для сбора всех уникальных названий полей
    all_fields = set()
    
    # Проходим по каждому элементу (словарю) в данных
    for item in data:
        # Добавляем все ключи текущего словаря в множество
        # Метод update добавляет все элементы из переданной коллекции
        all_fields.update(item.keys())
    
    # Преобразуем множество в отсортированный список
    # sorted() гарантирует алфавитный порядок полей в CSV
    fieldnames = sorted(all_fields)
    
    # Создаем объект Path для выходного CSV файла
    csv_path_obj = Path(csv_path)
    # Создаем все необходимые директории если они не существуют
    # parents=True - создает все родительские директории
    # exist_ok=True - не вызывает ошибку если директория уже существует
    csv_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Открываем CSV файл для записи
    with csv_path_obj.open('w', encoding='utf-8', newline='') as f:
        # Создаем DictWriter который будет записывать словари в CSV
        # fieldnames определяет порядок и набор колонок
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Записываем строку с заголовками колонок (первая строка CSV)
        writer.writeheader()
        
        # Проходим по всем объектам (словарям) из JSON данных
        for item in data:
            # Создаем строку для CSV: для каждого поля из fieldnames
            # берем значение из текущего объекта
            # item.get(field, '') - получает значение поля или пустую строку если поля нет
            # str() - преобразует все значения в строки для совместимости с CSV
            row = {field: str(item.get(field, '')) for field in fieldnames}
            
            # Записываем подготовленную строку в CSV файл
            writer.writerow(row)

def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV файл в JSON формат (список словарей).
    Принимает путь к CSV файлу и путь для сохранения JSON файла.
    """
    # Читаем данные из CSV файла с помощью нашей функции-помощника
    # data - список словарей, где ключи - заголовки колонок CSV
    # fieldnames - список заголовков колонок
    data, fieldnames = read_csv(csv_path)
    
    # Создаем объект Path для выходного JSON файла
    json_path_obj = Path(json_path)
    # Создаем все необходимые директории если они не существуют
    json_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Открываем JSON файл для записи
    with json_path_obj.open('w', encoding='utf-8') as f:
        # Записываем данные в JSON формате
        # data - список словарей для сериализации в JSON
        # ensure_ascii=False - разрешает запись кириллицы и других Unicode символов
        # indent=2 - форматирует JSON с отступами (2 пробела) для читаемости
        json.dump(data, f, ensure_ascii=False, indent=2)

# Блок для прямого запуска файла (тестирование функций)
if __name__ == "__main__":
    try:
        # Тестируем конвертацию JSON в CSV
        # "../data/samples/people.json" - относительный путь к исходному JSON файлу
        # "../data/out/people_from_json.csv" - относительный путь для сохранения CSV результата
        json_to_csv("../data/samples/people.json", "../data/out/people_from_json.csv")
        print("✓ JSON → CSV успешно")
        
        # Тестируем конвертацию CSV в JSON
        # "../data/samples/people.csv" - относительный путь к исходному CSV файлу
        # "../data/out/people_from_csv.json" - относительный путь для сохранения JSON результата
        csv_to_json("../data/samples/people.csv", "../data/out/people_from_csv.json")
        print("✓ CSV → JSON успешно")
        
        # Сообщаем пользователю где искать результаты конвертации
        print("Файлы созданы в src/data/out/")
        
    except Exception as e:
        # Обрабатываем любые исключения которые могут возникнуть при выполнении
        # и выводим понятное сообщение об ошибке
        print(f"❌ Ошибка: {e}")