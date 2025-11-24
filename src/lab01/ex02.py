a = input()
b = input()
a = a.replace(",", ".", 1)
b = b.replace(",", ".", 1)
a = float(a)
b = float(b)
sum = a + b
avg = (a + b) / 2
print(f"{sum:.2f}")
print(f"{avg:.2f}")
