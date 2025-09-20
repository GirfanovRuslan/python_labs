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
