# Лабораторная работа 5: Конвертация форматов данных

- [JSON <-> CSV](/src/lab05/json_csv.py)
- [CSV -> XLSX](/src/lab05/csv_xlsx.py)
- [Samples](/src/data/lab05/samples)
- [Out](/src/data/lab05/out)

## Реализованные функции

### 1. json_to_csv(json_path, csv_path)
Конвертирует JSON-файл в CSV формат.

**Особенности:**
- Поддерживает список словарей `[{...}, {...}]`
- Заполняет отсутствующие поля пустыми строками
- Порядок колонок - алфавитный
- Кодировка `UTF-8`
- Валидация входных данных

**Пример использования:**
```python
json_to_csv("src/data/lab05/samples/people.json", "src/data/lab05/out/people_from_json.csv")

### 2. csv_to_json(csv_path, json_path)
Конвертирует CSV-файл в JSON формат.

Особенности:
- Заголовок обязателен
- Значения сохраняются как строки
- Кодировка `UTF-8`
- Проверка наличия заголовка

Пример использования:
```python
csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")
```

### 3. csv_to_xlsx(csv_path, xlsx_path)
Конвертирует CSV-файл в XLSX формат.

Особенности:
- Использует библиотеку `openpyxl`
- Первая строка CSV становится заголовком
- Лист называется `"Sheet1"`
- Автоширина колонок (минимум 8 символов)
- Кодировка `UTF-8`

Пример использования:
```python
csv_to_xlsx("data/samples/cities.csv", "data/out/cities_from_csv.xlsx")
```


## Команды запуска

### Установка зависимостей 

#### Напрямую
```bash
pip install openpyxl
```

#### Через `requirements.txt`
```bash
pip install -r requirements.txt
```
- Эта команда просканирует файл `requirements.txt` и установит все перечисленные в нем пакеты (нужной версии)
    ```txt
    openpyxl==3.1.0 
    ```

### Запуск программ
```bash
python src/lab05/csv_xlsx.py
```
```bash
python src/lab05/json_csv.py
```

## Валидация и обработка ошибок

#### Проверяемые сценарии:

1. **Пустой JSON** → `ValueError: "Пустой JSON или неподдерживаемая структура"`
2. **CSV без заголовка** → `ValueError: "CSV файл не содержит заголовок"`
3. **Неподдерживаемая структура JSON** → `ValueError: "JSON должен содержать список объектов"`
4. **Отсутствующие поля** → заполняются пустыми строками
5. **Некорректные типы параметров** → `TypeError`
6. **Несуществующие файлы** → `FileNotFoundError`

#### Примеры обработки ошибок:

```python
# Пустой JSON
try:
    json_to_csv("data/samples/empty_json.json", "data/out/empty.csv")
except ValueError as e:
    print(f"Ошибка: {e}")  # "Пустой JSON или неподдерживаемая структура"

# CSV без заголовка  
try:
    csv_to_json("data/samples/no_header_csv.csv", "data/out/no_header.json")
except ValueError as e:
    print(f"Ошибка: {e}")  # "CSV файл не содержит заголовок"
```


## Результаты выполнения

### Входные данные:

#### people.json:
![people.json](/images/lab05/img06.png)

#### cities.csv:
![cities.csv](/images/lab05/img02.png)

#### people.csv:
![people.csv](/images/lab05/img05.png)

#### empty_json.json:
![empty_json.json](/images/lab05/img03.png)

#### no_header_csv.csv:
![no_header_csv.csv](/images/lab05/img04.png)

#### test_missing_fields.json:
![test_missing_fields.json](/images/lab05/img07.png)

### Выходные файлы:

#### people_from_json.csv:
![people_from_json.csv](/images/lab05/img10.png)

#### cities_from_csv.xlsx:
![cities_from_csv.xlsx](/images/lab05/img01.png)

#### people_from_csv.json:
![people_from_csv.json](/images/lab05/img09.png)

#### empty_from_json.csv:
`Ошибка: Пустой JSON или неподдерживаемая структура`

#### no_header_from_csv.json:
`Ошибка: CSV файл, вероятно, не содержит заголовок (эвритический подход)`

#### missing_fields_from_json.csv:
![missing_fields_from_json.csv](/images/lab05/img08.png)


## Особенности реализации

1. **Кодировка `UTF-8`** - используется везде для корректной работы с русскими символами
2. **Автоширина колонок** - в `XLSX` файлах колонки автоматически подстраиваются под содержимое
3. **Валидация данных** - строгая проверка входных параметров и структур данных
4. **Обработка ошибок** - информативные сообщения об ошибках для диагностики
5. **Создание директорий** - автоматическое создание выходных папок при необходимости