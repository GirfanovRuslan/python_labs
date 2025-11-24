import sys
import os
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.append("src")

from lab05.json_csv import json_to_csv, csv_to_json
from lab05.csv_xlsx import csv_to_xlsx


def validate_file_exists(file_path: str) -> Path:
    """Проверяет существование файла и возвращает Path объект"""
    if not file_path or not isinstance(file_path, str):
        raise ValueError(f"Путь к файлу должен быть непустой строкой: {file_path}")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    if not path.is_file():
        raise ValueError(f"{file_path} не является файлом")

    return path


def validate_directory_exists(dir_path: str) -> Path:
    """Проверяет существование директории"""
    if not dir_path or not isinstance(dir_path, str):
        raise ValueError(f"Путь к директории должен быть непустой строкой: {dir_path}")

    path = Path(dir_path)

    if not path.exists():
        raise FileNotFoundError(f"Директория {dir_path} не найдена")

    if not path.is_dir():
        raise ValueError(f"{dir_path} не является директорией")

    return path


def validate_file_extension(file_path: str, expected_extensions: list) -> None:
    """Проверяет расширение файла"""
    if not expected_extensions:
        raise ValueError("Список ожидаемых расширений не может быть пустым")

    path = validate_file_exists(file_path)

    ext = path.suffix.lower()
    expected_extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in expected_extensions
    ]

    if ext not in expected_extensions:
        expected_str = ", ".join(expected_extensions)
        raise ValueError(
            f"Ошибка: файл {file_path} должен иметь расширение {expected_str}"
        )


def ensure_directory(dir_path: str) -> Path:
    """Создает директорию если её нет"""
    if not dir_path or not isinstance(dir_path, str):
        raise ValueError(f"Путь к директории должен быть непустой строкой: {dir_path}")

    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def cleanup_on_error(file_path: str) -> None:
    """Удаляет файл если он был частично создан при ошибке"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   🗑️ Удален частично созданный файл: {file_path}")
    except Exception:
        pass  # Игнорируем ошибки при удалении


def main():
    print("=== ТЕСТ ЛР5 ===")

    # Создаем выходную директорию заранее
    try:
        ensure_directory("data/lab05/out/")
        print("   📁 Создана выходная директория: data/lab05/out/")
    except Exception as e:
        print(f"❌ Ошибка создания директории: {e}")
        return

    try:
        # Тест 1: JSON → CSV
        print("1. JSON → CSV...")
        try:
            json_to_csv(
                "data/lab05/samples/people.json", "data/lab05/out/people_from_json.csv"
            )
            print("   ✓ Успешно")
        except Exception as e:
            cleanup_on_error("data/lab05/out/people_from_json.csv")
            raise e

        # Тест 2: CSV → JSON
        print("2. CSV → JSON...")
        try:
            validate_file_extension("data/lab05/samples/people.csv", [".csv"])
            validate_file_extension("data/lab05/out/people_from_csv.json", [".json"])
            csv_to_json(
                "data/lab05/samples/people.csv", "data/lab05/out/people_from_csv.json"
            )
            print("   ✓ Успешно")
        except Exception as e:
            cleanup_on_error("data/lab05/out/people_from_csv.json")
            raise e

        # Тест 3: CSV → XLSX
        print("3. CSV → XLSX...")
        try:
            validate_file_extension("data/lab05/samples/people.csv", [".csv"])
            validate_file_extension("data/lab05/out/people.xlsx", [".xlsx"])
            csv_to_xlsx("data/lab05/samples/people.csv", "data/lab05/out/people.xlsx")
            print("   ✓ Успешно")
        except Exception as e:
            cleanup_on_error("data/lab05/out/people.xlsx")
            raise e

        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("📁 Проверь файлы в: data/lab05/out/")

        # Показываем созданные файлы
        out_dir = Path("data/lab05/out/")
        if out_dir.exists():
            files = list(out_dir.glob("*"))
            if files:
                print("\n📄 Созданные файлы:")
                for file in files:
                    size = file.stat().st_size
                    print(f"   • {file.name} ({size} байт)")

    except FileNotFoundError as e:
        print(f"❌ Файл не найден: {e}")
        print("   🔍 Проверь пути к файлам в папке data/lab05/samples/")
    except PermissionError as e:
        print(f"❌ Ошибка доступа: {e}")
        print("   🔒 Проверь права доступа к файлам")
    except ValueError as e:
        print(f"❌ Ошибка валидации: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        print("   🐛 Подробности:", type(e).__name__)


if __name__ == "__main__":
    main()
