# python_labs

## 1 задание
```python
name=input()
age=int(input())
print(f"Привет {name}! Через год тебе будет {age+1}.")
```

![alt text](src/images/lab01/ex01.png)

## 2 задание
``` python
a=input()
b=input()
a=a.replace(",",".",1)
b=b.replace(",",".",1)
a=float(a)
b=float(b)
sum=a+b
avg=(a+b)/2
print(f"{sum:.2f}")
print(f"{avg:.2f}")
```
![alt text](src/images/lab01/ex02.png)

## 3 задание

```python
price=float(input())
discount=float(input())
vat=float(input())
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
print("База после скидки:",f"{base:.2f} ₽")
print("НДС:",f"{vat_amount:.2f} ₽")
print("Итого к оплате:",f"{total:.2f} ₽")
```
![alt text](src/images/lab01/ex03.png)
## 4 задание
```python
minut=int(input())
hour=minut//60
minut=minut-(60*hour)
print(f"{hour}:{minut}")
```

![alt text](src/images/lab01/ex04.png)


# 5 задание

```python
FIO=input()
k=0
b=[]
c=[]
x=[]
t=len(FIO)
for i in FIO:
    if i==" ":
        k=k+1
if k!=2:
    t=t-k+2
a=FIO.split(None)
b.append(a[0])
c.append(a[1])
x.append(a[2])
q=b[0]
w=c[0]
e=x[0]
print("Инициалы:",q[0],w[0],e[0],sep="")
print("Длина символов:",t)
```
![alt text](src/images/lab01/ex05.png)

# 6 задание
```python
print("Введите число учащихся:")
n=int(input())
k=0
c=0
for a in range(n):
    print("А теперь введите фамилию, имя, возраст, и формат обучения: False ot True")
    s=input()
    d=s.split()
    forma=d[3]
    if forma=="True":
        k=k+1
    else:
        c=c+1
print(f"Очный:{k} Заочный:{c}")
```
![alt text](src/images/lab01/ex06.png)




# Лабораторная работа №2
## Задание 1
```python
def min_max(nums: list[float | int]):
    if not nums:
        return ("Value Error")
    else:
        min_val = min(nums)
        max_val = max(nums)
        return (min_val,max_val)
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([1.5,2,2.0,-3.1]))
print(min_max([]))
```
![alt text](src/images/lab02/lab02ex01.png)

## Задание 2
```python
def unique_sorted(nums: list[float | int]):
    return (list(sorted(set(nums))))
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
```
![alt text](src/images/lab02/lab02ex02.png)

## Задание 3
```python
def flatten(mat: list[list | tuple]):
    flattened_list = []
    for row in mat:
        if isinstance(row, (list, tuple)):
            flattened_list.extend(row)
        else:
            return ("TypeError")
    return (flattened_list)
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [],[2, 3]]))
print(flatten([[1, 2], "ab"]))
```
![alt text](src/images/lab02/lab02ex03.png)

## Задание 4
```python
def transpose(mat: list[list[float | int]]):
    if not mat:
        return []
    rows=len(mat)
    cols=len(mat[0])
    for row in mat:
        if len(row)!=cols:
            return ("ValueError")
    teleport_mat = [[mat[i][j] for i in range(rows)] for j in range(cols)]
    return teleport_mat
print(transpose([[1, 2, 3]]))
print(transpose([[1],[2], [3]]))
print(transpose([[1,2],[3,4]]))
print(transpose([[1,2],[3]]))
print(transpose([[]]))
```
![alt text](src/images/lab02/lab02ex04.png)

## Задание 5
```python
def row_sums(mat: list[list[float | int]]):
    if not mat:
        return []
    rows = len(mat)
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            return ("ValueError")
    sums=[sum(row) for row in mat]
    return sums
print(row_sums([[1,2,3], [4,5,6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0,0], [0,0]]))
print(row_sums([[1,2], [3]]))
```
![alt text](src/images/lab02/lab02ex05.png)

## Задание 6
```python
def col_sums(mat: list[list[float | int]]):
    if not mat:
        return []
    rows = len(mat)
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            return ("ValueError")
    sums = [sum(mat[i][j] for i in range(rows)) for j in range(cols)]
    return sums
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
```
![alt text](src/images/lab02/lab02ex06.png)

## Задание 7
```python
def format_record(rec: tuple[str, str, float]):
    fio, group, gpa = rec
    parts = fio.strip().split()
    family = parts[0]
    initials = ""
    for part in parts[1:]:
        initials += part[0].upper() + "."
    if not initials:
        initials = ""
    form_gpa=f"{gpa:.2f}"
    return f"{family} {initials}, гр. {group}, GPA {form_gpa}"
print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
```
![alt text](src/images/lab02/lab02ex07.png)