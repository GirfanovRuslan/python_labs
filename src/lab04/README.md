<div align="center">

# <span class="pulse-text">🎬 Вы смотрите мою четвертую лабу!</span>

<style>
.pulse-text {
  animation: pulse 3s infinite;
  color: #ff00d4ff;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(251, 255, 0, 0.5);
}

@keyframes pulse {
  0% { 
    opacity: 0;
    transform: scale(0.8);
  }
  50% { 
    opacity: 1;
    transform: scale(1.1);
  }
  100% { 
    opacity: 0;
    transform: scale(0.8);
  }
}
</style>

</div>

## Код программы

- **[io_txt_csv.py](src/lab04/io_txt_csv.py)** - модуль для работы с файлами
- **[text_report.py](src/lab04/text_report.py)** - скрипт генерации отчетов

## Запуск
![alt text](../../images/lab04/lab04A.png)
![alt text](/images/lab04/lab04.png)
## Кодировки файлов

- **По умолчанию:** UTF-8
- **Для других кодировок:** 
  ```python
  read_text("file.txt", encoding="cp1251")  # Windows-1251
  read_text("file.txt", encoding="koi8-r")  # KOI8-R
