import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab04.io_txt_csv import read_text, write_csv
from lib.text import normalize, tokenize, count_freq, top_n

# Основной код в 3 строки:
text = read_text("src/data/lab04/input.txt")
freq = count_freq(tokenize(normalize(text)))
write_csv(sorted(freq.items(), key=lambda x: (-x[1], x[0])), 
          "src/data/lab04/report.csv", 
          header=("word", "count"))

# Статистика
print(f"Слов: {sum(freq.values())}, Уникальных: {len(freq)}")
print("Топ-5:", *[f"{w}:{c}" for w, c in top_n(freq, 5)])
