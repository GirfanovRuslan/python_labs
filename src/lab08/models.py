from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        try:
            self.birthdate = datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Неверный формат даты рождения: {self.birthdate}, должен быть YYYY-MM-DD")
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"GPA должно быть в пределах от 0 до 5, получено: {self.gpa}")

    def age(self) -> int:
        """Вычисляем возраст студента по его дате рождения"""
        today = date.today()
        age = today.year - self.birthdate.year
        if today.month < self.birthdate.month or (today.month == self.birthdate.month and today.day < self.birthdate.day):
            age -= 1
        return age

    def to_dict(self) -> dict:
        """Сериализация объекта в словарь"""
        return {
            "fio": self.fio,
            "birthdate": self.birthdate.strftime("%Y-%m-%d"),
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Десериализация объекта из словаря"""
        return cls(
            fio=d['fio'],
            birthdate=d['birthdate'],
            group=d['group'],
            gpa=d['gpa']
        )

    def __str__(self):
        """Красивая строка для вывода информации о студенте"""
        return f"{self.fio}, {self.group}, GPA: {self.gpa}"
