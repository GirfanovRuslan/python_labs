<div align="center">

# ✨ **Вы смотрите мою шестую лабу!** ✨

</div>

### 🔄 Модуль `cli_convert.py` - конвертация данных
### Команда: `json2csv`

**Назначение:** Конвертирует JSON файл в CSV формат
```bash
py src/lab06/cli_convert.py json2csv --in data/lab05/samples/people.json --out data/lab06/out/from_cli.csv
```
## Было:
![alt text](<../../images/lab06/lab06 jsoncsv1.png>)
## Запуск кода
![alt text](<../../images/lab06/lab06 jsoncsv2.png>)
## Стало:
![alt text](<../../images/lab06/lab06 jsoncsv.png>)

## Команда: csv2json
### Назначение: Конвертирует CSV файл в JSON формат
``` bash
py src/lab06/cli_convert.py csv2json --in data/lab05/samples/people.csv --out data/lab06/out/from_cli.json
```
## Было:
![alt text](<../../images/lab06/lab06 csvjson2.png>)
## Запуск кода
![alt text](<../../images/lab06/lab06 csvjson1.png>)
## Стало:
![alt text](<../../images/lab06/lab06 csvjson3.png>)

## Команда: csv2xlsx
### Назначение: Конвертирует CSV файл в XLSX формат (Excel)
```bash
py src/lab06/cli_convert.py csv2xlsx --in data/lab05/samples/people.csv --out data/lab06/out/from_cli.xlsx
```
## Было:
![alt text](<../../images/lab06/lab06 csvxsl2.png>)
## Запуск кода
![alt text](<../../images/lab06/lab06 csvxsl1.png>)
## Стало:
![alt text](<../../images/lab06/lab06 csvxsl3.png>)


# 📊 Модуль cli_text.py - работа с текстом
## Команда: stats
### Назначение: Анализ частот слов в текстовом файле
```bash
py src/lab06/cli_text.py stats --in data/lab06/out/text.txt --top 3
```
## Файл с текстом 
![alt text](<../../images/lab06/lab06 stats2.png>)
## Запуск кода
![alt text](<../../images/lab06/lab06 stats1.png>)

## Команда: cat
### Назначение: Вывод содержимого файла с опциональной нумерацией
```bash
py src/lab06/cli_text.py cat --in data/lab06/out/text.txt -n
```
## Файл с текстом 
![alt text](<../../images/lab06/lab06 stats2.png>)
## Запуск кода
![alt text](<../../images/lab06/lab06 cat1.png>)


# 🚨 Демонстрация обработки ошибок