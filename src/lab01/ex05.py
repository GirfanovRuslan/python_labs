FIO = input()
k = 0
b = []
c = []
x = []
t = len(FIO)
for i in FIO:
    if i == " ":
        k = k + 1
if k != 2:
    t = t - k + 2
a = FIO.split(None)
b.append(a[0])
c.append(a[1])
x.append(a[2])
q = b[0]
w = c[0]
e = x[0]
print("Инициалы:", q[0], w[0], e[0], sep="")
print("Длина символов:", t)
