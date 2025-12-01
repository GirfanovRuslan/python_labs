import os
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.lab08.serialize import students_from_json, students_to_json

def main():
    print("Программа запущена!")  # Отладочное сообщение

    try:
        # 1. Чтение данных
        print("\n1. Чтение студентов из файла...")
        input_file = "data/lab08/students_input.json"
        
        # Проверяем, существует ли файл
        if not os.path.exists(input_file):
            print(f"Ошибка: Файл {input_file} не найден.")
            return
        
        students = students_from_json(input_file)
        print(f"✓ Успешно прочитано {len(students)} студентов из {input_file}")
        
        # 2. Вывод информации
        print("\n2. Список студентов:")
        for i, student in enumerate(students, 1):
            print(f"\n  {i}. {student}")
            print(f"     • Возраст: {student.age()} лет")
            print(f"     • Группа: {student.group}")
            print(f"     • Средний балл: {student.gpa}")
        
        # 3. Сохранение данных
        print("\n3. Сохранение студентов в файл...")
        output_file = "data/lab08/students_output.json"
        students_to_json(students, output_file)
        print(f"✓ Данные сохранены в {output_file}")
        
        # 4. Сравнение файлов
        print("\n4. Сравнение размеров файлов:")
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        print(f"   Входной файл: {input_size} байт")
        print(f"   Выходной файл: {output_size} байт")
        
        print(f"\n{'='*50}")
        print("Программа успешно завершена! ✓")
        print(f"{'='*50}")
        
    except FileNotFoundError as e:
        print(f"\n✗ Ошибка: Файл не найден: {e}")
        print("Убедитесь, что файл students_input.json существует в data/lab08/")
        
    except ImportError as e:
        print(f"\n✗ Ошибка импорта: {e}")
        print("Проверьте структуру папок и названия модулей")
        
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Завершающий вывод: вызываем main()")  # Это поможет понять, что программа заходит сюда
    main()
