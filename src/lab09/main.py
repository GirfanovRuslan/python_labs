import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lab09.group import Group
from src.lab08.models import Student

def print_students(title, students):
    """Красиво вывести список студентов"""
    print("\n" + "="*60)
    print(f"📋 {title}")
    print("="*60)
    if not students:
        print("Студентов нет")
    else:
        for i, s in enumerate(students, 1):
            # Проверяем формат даты
            birthdate = s.birthdate
            if hasattr(birthdate, 'strftime'):
                birthdate = birthdate.strftime("%Y-%m-%d")
            
            print(f"{i:2}. {s.fio:25} | {birthdate:10} | {s.group:10} | {s.gpa:.2f}")

def test_crud_operations():
    """Тестирование CRUD операций"""
    print("🚀 Тестирование класса Group (CRUD операции)")
    print("-" * 60)
    
    # Инициализируем группу
    csv_path = "data/lab09/students.csv"
    print(f"📁 Используем файл: {csv_path}")
    
    # Удаляем старый файл для чистого теста
    if os.path.exists(csv_path):
        os.remove(csv_path)
    
    g = Group(csv_path)
    
    # 1. Проверяем пустой список
    print("\n1. Начальное состояние (должно быть пусто):")
    print_students("Все студенты:", g.list())
    
    # 2. Добавляем студентов
    print("\n2. Добавление студентов:")
    
    students_to_add = [
        Student("Иванов Иван Иванович", "2003-10-10", "БИВТ-21-1", 4.3),
        Student("Петров Петр Петрович", "2002-05-15", "БИВТ-21-2", 3.8),
        Student("Сидорова Анна Владимировна", "2003-03-20", "БИВТ-21-1", 4.9),
    ]
    
    for student in students_to_add:
        if g.add(student):
            print(f"   ✅ Добавлен: {student.fio}")
    
    print_students("После добавления 3-х студентов:", g.list())
    
    # 3. Поиск студентов
    print("\n3. Поиск студентов:")
    
    search_queries = ["Иван", "Петр", "Анна"]
    for query in search_queries:
        found = g.find(query)
        print(f"   Поиск '{query}': найдено {len(found)} студентов")
        for s in found:
            print(f"     - {s.fio}")
    
    # 4. Обновление студента
    print("\n4. Обновление данных студента:")
    
    if g.update("Петров Петр Петрович", gpa=4.1, group="БИВТ-21-5"):
        print("   ✅ Данные Петрова обновлены")
    
    print_students("После обновления:", g.list())
    
    # 5. Удаление студента
    print("\n5. Удаление студента:")
    
    if g.remove("Сидорова Анна Владимировна"):
        print("   ✅ Сидорова удалена")
    
    print_students("После удаления:", g.list())
    
    # 6. Показываем содержимое файла
    print("\n6. Содержимое CSV файла:")
    print("-" * 40)
    with open(csv_path, "r", encoding="utf-8") as f:
        print(f.read())
    
    print("\n" + "="*60)
    print("✅ Все CRUD операции протестированы успешно!")

if __name__ == "__main__":
    test_crud_operations()