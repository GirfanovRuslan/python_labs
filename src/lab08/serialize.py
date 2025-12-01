import json
from .models import Student

def students_to_json(students, path):
    """Сериализует список студентов в JSON файл"""
    data = [s.to_dict() for s in students]  # Преобразуем студентов в словари
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path):
    """Десериализует список студентов из JSON файла"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Загружаем данные из JSON файла
        students = [Student.from_dict(item) for item in data]  # Преобразуем словари обратно в объекты Student
    return students
