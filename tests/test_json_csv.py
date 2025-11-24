import pytest
import json
import csv
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json


class TestJsonToCsv:
    def test_basic_conversion(self, tmp_path):
        # tmp_path - временная папка, создается автоматически для каждого теста
        src = tmp_path / "test.json"  # Создаем путь к исходному файлу
        dst = tmp_path / "test.csv"  # Создаем путь к целевому файлу

        # Тестовые данные для конвертации
        data = [
            {"name": "Alice", "age": 22, "city": "Moscow"},
            {"name": "Bob", "age": 25, "city": "SPb"},
        ]

        # Записываем тестовые данные в JSON файл
        src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        # ВЫПОЛНЯЕМ тестируемую функцию - конвертируем JSON в CSV
        json_to_csv(str(src), str(dst))

        # ПРОВЕРЯЕМ результат - читаем созданный CSV файл
        with open(dst, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # Читаем CSV как словари
            rows = list(reader)

        # УТВЕРЖДАЕМ что:
        assert len(rows) == 2  # Количество строк совпадает
        assert set(rows[0].keys()) == {"name", "age", "city"}  # Заголовки правильные
        assert rows[0]["name"] == "Alice"  # Данные первой строки верные
        assert rows[1]["name"] == "Bob"  # Данные второй строки верные

    def test_file_not_found(self):
        # Тест: проверяем обработку отсутствующего файла
        with pytest.raises(
            FileNotFoundError
        ):  # ОЖИДАЕМ, что функция выбросит эту ошибку
            json_to_csv(
                "nonexistent.json", "output.csv"
            )  # Вызываем с несуществующим файлом

    def test_invalid_json(self, tmp_path):
        # Тест: проверяем обработку некорректного JSON
        src = tmp_path / "invalid.json"
        dst = tmp_path / "output.csv"

        # Создаем файл с неправильным JSON
        src.write_text("{ invalid json }", encoding="utf-8")

        # ОЖИДАЕМ, что функция выбросит ValueError при чтении некорректного JSON
        with pytest.raises(ValueError):
            json_to_csv(str(src), str(dst))


class TestCsvToJson:
    def test_basic_conversion(self, tmp_path):
        # Тест: конвертация CSV в JSON
        src = tmp_path / "test.csv"
        dst = tmp_path / "test.json"

        # Создаем тестовый CSV файл
        csv_content = "name,age,city\nAlice,22,Moscow\nBob,25,SPb"
        src.write_text(csv_content, encoding="utf-8")

        # ВЫПОЛНЯЕМ тестируемую функцию
        csv_to_json(str(src), str(dst))

        # ПРОВЕРЯЕМ результат - читаем созданный JSON
        with open(dst, "r", encoding="utf-8") as f:
            data = json.load(f)  # Парсим JSON

        # УТВЕРЖДАЕМ что:
        assert len(data) == 2  # Количество записей совпадает
        assert data[0] == {
            "name": "Alice",
            "age": "22",
            "city": "Moscow",
        }  # Первая запись верна
        assert data[1] == {
            "name": "Bob",
            "age": "25",
            "city": "SPb",
        }  # Вторая запись верна
        # Примечание: age стал строкой "22" а не числом 22 - это нормально для CSV→JSON

    def test_file_not_found(self):
        # Тест: проверяем обработку отсутствующего CSV файла
        with pytest.raises(FileNotFoundError):
            csv_to_json("nonexistent.csv", "output.json")

    def test_empty_csv(self, tmp_path):
        # Тест: проверяем обработку пустого CSV файла
        src = tmp_path / "empty.csv"
        dst = tmp_path / "output.json"

        # Создаем пустой файл
        src.write_text("", encoding="utf-8")

        # ОЖИДАЕМ ValueError при попытке конвертировать пустой файл
        with pytest.raises(ValueError):
            csv_to_json(str(src), str(dst))


class TestRoundTrip:
    def test_json_csv_json(self, tmp_path):
        # Тест: полный цикл JSON → CSV → JSON (данные должны сохраниться)
        original_data = [{"name": "Test", "value": 42}, {"name": "Demo", "value": 24}]

        # Создаем пути к файлам
        json1 = tmp_path / "test1.json"
        csv_file = tmp_path / "test.csv"
        json2 = tmp_path / "test2.json"

        # Записываем исходные данные в JSON
        json1.write_text(
            json.dumps(original_data, ensure_ascii=False), encoding="utf-8"
        )

        # Выполняем двойную конвертацию: JSON → CSV → JSON
        json_to_csv(str(json1), str(csv_file))
        csv_to_json(str(csv_file), str(json2))

        # Читаем финальный JSON
        with open(json2, "r", encoding="utf-8") as f:
            final_data = json.load(f)

        # ПРОВЕРЯЕМ что данные сохранились:
        assert len(final_data) == len(original_data)  # Количество записей не изменилось
        assert final_data[0]["name"] == original_data[0]["name"]  # Имена совпадают
        # Примечание: числа могли стать строками - это нормально для CSV
