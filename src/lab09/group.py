import csv
from pathlib import Path
from datetime import datetime
from src.lab08.models import Student


class Group:
    HEADER = ["fio", "birthdate", "group", "gpa"]

    def __init__(self, storage_path):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Создать файл с заголовком, если не существует"""
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADER)

    def _parse_date(self, date_str):
        """Преобразовать строку с датой в формат YYYY-MM-DD"""
        try:
            # Пробуем разные форматы
            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y"]:
                try:
                    dt = datetime.strptime(date_str.strip(), fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return date_str.strip()  # Если не удалось распарсить, возвращаем как есть
        except:
            return date_str.strip()

    def _read_all(self):
        """Прочитать всех студентов из CSV"""
        students = []
        if self.path.exists() and self.path.stat().st_size > 0:
            with self.path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Очищаем и парсим дату
                    clean_date = self._parse_date(row["birthdate"])
                    
                    students.append(
                        Student(
                            fio=row["fio"].strip(),
                            birthdate=clean_date,
                            group=row["group"].strip(),
                            gpa=float(row["gpa"]),
                        )
                    )
        return students

    def _write_all(self, students):
        """Записать всех студентов в CSV"""
        with self.path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for s in students:
                # Преобразуем дату обратно в строку
                if hasattr(s.birthdate, 'strftime'):
                    birthdate_str = s.birthdate.strftime("%Y-%m-%d")
                else:
                    birthdate_str = str(s.birthdate)
                
                writer.writerow([s.fio, birthdate_str, s.group, s.gpa])

    def list(self):
        """Получить список всех студентов"""
        return self._read_all()

    def add(self, student):
        """Добавить нового студента"""
        # Проверяем, нет ли уже студента с таким ФИО
        existing = self._read_all()
        for s in existing:
            if s.fio == student.fio:
                print(f"⚠️  Внимание: студент с ФИО '{student.fio}' уже существует")
                return False
        
        # Добавляем нового студента
        with self.path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            
            # Преобразуем дату для записи
            if hasattr(student.birthdate, 'strftime'):
                birthdate_str = student.birthdate.strftime("%Y-%m-%d")
            else:
                birthdate_str = str(student.birthdate)
            
            writer.writerow([student.fio, birthdate_str, student.group, student.gpa])
        return True

    def find(self, substr):
        """Найти студентов по подстроке в ФИО"""
        substr = substr.lower()
        return [s for s in self._read_all() if substr in s.fio.lower()]

    def remove(self, fio):
        """Удалить студента по ФИО"""
        students = self._read_all()
        initial_count = len(students)
        students = [s for s in students if s.fio != fio]
        
        if len(students) < initial_count:
            self._write_all(students)
            return True
        return False

    def update(self, fio: str, **fields):
        """Обновить данные студента"""
        students = self._read_all()
        updated = False
        
        for student in students:
            if student.fio == fio:
                for key, value in fields.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                    else:
                        raise ValueError(f"Недопустимое поле: {key}")
                updated = True
                break
        
        if updated:
            self._write_all(students)
        else:
            print(f"⚠️  Внимание: студент с ФИО '{fio}' не найден")
        
        return updated