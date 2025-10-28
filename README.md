# 🐍 Python Labs

<div align="center">

<!-- Анимированный заголовок -->
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=600&lines=🚀+Лабораторные+работы+от+Руслана;💻+Python+Developer;🎯+С+любовью+к+коду" alt="Типизированный заголовок" />

<!-- Бейджи -->
<p>
  <img src="https://img.shields.io/badge/Студент-Разработчик-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.12-green?style=for-the-badge&logo=python" />
</p>

</div>

<div align="center">

---

## 📜 **Авторские права**

<div style="font-size: 0.9em; color: #666;">

**© 2025 Руслан. Все права защищены.**  
*Код предназначен только для ознакомления.  
Любое копирование или использование без разрешения автора запрещено.*

</div>

</div>




# Лабораторная работа №2
## Задание 1
```python
def min_max(nums: list[float | int]):
    if not nums:
        raise ValueError
    else:
        min_val = min(nums)
        max_val = max(nums)
        return (min_val,max_val)
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([1.5,2,2.0,-3.1]))
print(min_max([]))
```
![alt text](src/images/lab02/lab02ex01.png)
## Задание 2
```python
def unique_sorted(nums: list[float | int]):
    return (list(sorted(set(nums))))
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
```
![alt text](src/images/lab02/lab02ex02.png)

## Задание 3
```python
def flatten(mat: list[list | tuple]):
    flattened_list = []
    for row in mat:
        if isinstance(row, (list, tuple)):
            flattened_list.extend(row)
        else:
            raise TypeError
    return (flattened_list)
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [],[2, 3]]))
print(flatten([[1, 2], "ab"]))
```
![alt text](src/images/lab02/lab02ex03.png)

## Задание 4
```python
def transpose(mat: list[list[float | int]]):
    if not mat:
        return []
    rows=len(mat)
    cols=len(mat[0])
    for row in mat:
        if len(row)!=cols:
            raise ValueError
    teleport_mat = [[mat[i][j] for i in range(rows)] for j in range(cols)]
    return teleport_mat
print(transpose([[1, 2, 3]]))
print(transpose([[1],[2], [3]]))
print(transpose([[1,2],[3,4]]))
print(transpose([[1,2],[3]]))
print(transpose([[]]))
```
![alt text](src/images/lab02/lab02ex04.png)

## Задание 5
```python
def row_sums(mat: list[list[float | int]]):
    if not mat:
        return []
    rows = len(mat)
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError
    sums=[sum(row) for row in mat]
    return sums
print(row_sums([[1,2,3], [4,5,6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0,0], [0,0]]))
print(row_sums([[1,2], [3]]))
```
![alt text](src/images/lab02/lab02ex05.png)

## Задание 6
```python
def col_sums(mat: list[list[float | int]]):
    if not mat:
        return []
    rows = len(mat)
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError
    sums = [sum(mat[i][j] for i in range(rows)) for j in range(cols)]
    return sums
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
```
![alt text](src/images/lab02/lab02ex06.png)

## Задание 7
```python
def format_record(rec: tuple[str, str, float]):
    fio, group, gpa = rec
    if not isinstance(fio, str) or not fio.strip():
        raise ValueError("ФИО должно быть непустой строкой.")
    if not isinstance(group, str) or not group.strip():
        raise ValueError("Группа должна быть непустой строкой.")
    if not isinstance(gpa, (int, float)):
        raise ValueError("GPA должно быть числом.")
    parts = fio.strip().split()
    family = parts[0]
    family=(family.title())
    initials = ""
    for part in parts[1:]:
        initials += part[0].upper() + "."
    if not initials:
        initials = ""
    form_gpa=f"{gpa:.2f}"
    return f"{family} {initials}, гр. {group}, GPA {form_gpa}"
print(format_record((34141, "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))

```
![alt text](src/images/lab02/lab02ex07.png)

# Лабораторная работа №4

## Код программы

- **[io_txt_csv.py](src/lab04/io_txt_csv.py)** - модуль для работы с файлами
- **[text_report.py](src/lab04/text_report.py)** - скрипт генерации отчетов

## Запуск
![alt text](src/images/lab04/lab04A.png)
![alt text](src/images/lab04/lab04.png)
## Кодировки файлов

- **По умолчанию:** UTF-8
- **Для других кодировок:** 
  ```python
  read_text("file.txt", encoding="cp1251")  # Windows-1251
  read_text("file.txt", encoding="koi8-r")  # KOI8-R



# 🔹 [Лабораторная работа 5: Конвертация форматов данных](/src/lab05/README.md)
- **JSON ↔ CSV** - взаимная конвертация между структурированными и табличными данными
- **CSV → XLSX** - экспорт табличных данных в Excel формат
- **Валидация данных** - обработка ошибок и проверка целостности
- **Автоформатирование** - автоматическая настройка ширины колонок в Excel



####  Основные возможности:
- Поддержка русского языка (UTF-8 кодировка)
- Автоматическое создание директорий
- Информативные сообщения об ошибках
- Алфавитный порядок колонок в CSV

# Кликай сюда
[Вся инфа про лабу 5](src/lab05/README.md) 
<div align="center">

---

## 💝 Поддержать автора

<div style="font-size: 1.1em;">

✨ **Хочешь сказать спасибо?**  
💌 **Напиши в Telegram:** [@Rusic4k](https://t.me/rusic4k)  
🌟 **Или просто поставь звездочку репозиторию!**

</div>

<br>

[![Telegram](https://img.shields.io/badge/💬_Написать_автору-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/rusic4k)
[![GitHub Star](https://img.shields.io/badge/⭐_Поставить_звезду-ffd700?style=for-the-badge&logo=github&logoColor=black)](https://github.com/yourusername)

</div>