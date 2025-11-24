minut = int(input())
hour = minut // 60
minut = minut - (60 * hour)
print(f"{hour}:{minut}")
