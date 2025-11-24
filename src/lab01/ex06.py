print("Введите число учащихся:")
n = int(input())
k = 0
c = 0
for a in range(n):
    print("А теперь введите фамилию, имя, возраст, и формат обучения: False ot True")
    s = input()
    d = s.split()
    forma = d[3]
    if forma == "True":
        k = k + 1
    else:
        c = c + 1
print(f"Очный:{k} Заочный:{c}")
