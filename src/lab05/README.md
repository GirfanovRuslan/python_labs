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
csv_to_xlsx("src/data/lab05/samples/people.csv", "src/data/lab05/out/people.xlsx")
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

#### Пустой JSON
```python
try:
    json_to_csv("src/data/lab05/samples/empty.json", "src/data/lab05/out/empty.csv")
except ValueError as e:
    print(f"Ошибка: {e}")
```

### CSV без заголовка  
```python
try:
    csv_to_json("src/data/lab05/samples/no_header.csv", "src/data/lab05/out/no_header.json")
except ValueError as e:
    print(f"Ошибка: {e}")
```


## Результаты выполнения

### Входные данные:

#### people.json:
![alt text](<../images/lab05/lab05 1.png>)
#### cities.csv:
![alt text](<../images/lab05/lab05 3.png>)
#### people.csv:
![alt text](<../images/lab05/lab05 2.png>)


### Выходные файлы:

#### people_from_json.csv:
![alt text](<../images/lab05/lab05 4.png>)

#### cities_from_csv.xlsx:
![alt text](<../images/lab05/lab05 5.png>)

#### people_from_csv.json:
![alt text](<../images/lab05/lab05 6.png>)


## Особенности реализации

1. **Кодировка `UTF-8`** - используется везде для корректной работы с русскими символами
2. **Автоширина колонок** - в `XLSX` файлах колонки автоматически подстраиваются под содержимое
3. **Валидация данных** - строгая проверка входных параметров и структур данных
4. **Обработка ошибок** - информативные сообщения об ошибках для диагностики
5. **Создание директорий** - автоматическое создание выходных папок при необходимости