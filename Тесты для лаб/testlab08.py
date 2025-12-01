from src.lab08.models import Student

# Простое тестирование прямо в интерпретаторе Python
print("Тестирование класса Student")
print("=" * 40)

# Создание объектов
try:
    student1 = Student(
        fio="Иванов Иван Иванович",
        birthdate="2002-05-15",
        group="SE-01",
        gpa=4.5
    )
    print(f"✓ Создан студент: {student1}")
    print(f"Возраст: {student1.age()} лет")
except ValueError as e:
    print(f"✗ Ошибка: {e}")

# Тест валидации
print("\nТест валидации:")
try:
    bad_student = Student(
        fio="Тестовый Студент",
        birthdate="неправильная дата",  # ошибка формата
        group="TEST-01",
        gpa=4.0
    )
except ValueError as e:
    print(f"✓ Поймана ошибка валидации даты: {e}")

try:
    bad_student2 = Student(
        fio="Тестовый Студент",
        birthdate="2000-01-01",
        group="TEST-01",
        gpa=10.0  # ошибка диапазона (должно быть 0-5)
    )
except ValueError as e:
    print(f"✓ Поймана ошибка валидации GPA: {e}")

# Тест сериализации
print("\nТест сериализации:")
student2 = Student(
    fio="Петрова Анна Сергеевна",
    birthdate="2003-11-22",
    group="CS-03",
    gpa=4.8
)

print(f"Словарь: {student2.to_dict()}")
print(f"Строковое представление: {student2}")