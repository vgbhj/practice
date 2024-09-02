import random

# Функция для чтения строк из файла и формирования массива
def read_file_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Чтение файлов
dubers_lines = read_file_to_list('dubers.txt')
roles_lines = read_file_to_list('roles.txt')

print(dubers_lines)

# Перемешивание строк из dobber.txt
random.shuffle(dubers_lines)

# Если строк в dobber.txt меньше, чем в roles.txt, дублируем список dobber_lines
if len(dubers_lines) < len(roles_lines):
    dubers_lines *= (len(roles_lines) // len(dubers_lines)) + 1

# Присвоение случайных строк
assigned_pairs = []
for i, role in enumerate(roles_lines):
    assigned_pairs.append((role.strip(), dubers_lines[i % len(dubers_lines)].strip()))

# Вывод результата
for role, dobber in assigned_pairs:
    print(f"{role} -> {dobber}")
