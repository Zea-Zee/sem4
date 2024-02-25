import subprocess
import pandas as pd
import re

# Создаем список флагов для CPU
cpu_flags = ['1', '1-2', '1-4', '1-8', '12', '1-16',
             '1-20', '1-24', '1-28', '1-32', '1-36', '1-40']

# Создаем список размеров
sizes = [20000, 40000]

# Создаем список словарей для хранения данных
data = []

# Проходим по каждому размеру и запускаем программу DGEMV для каждого флага процессора
for size in sizes:
    row_data = {'Size': size}
    for flag in cpu_flags:
        # Формируем команду для запуска программы с заданными флагами и размерами
        command = f"taskset -c {flag} ./DGEMV {size} {size}"
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        # Получаем результат и извлекаем время выполнения из последней строки вывода программы
        output_lines = result.stdout.splitlines()
        last_line = output_lines[-1]
        match = re.search(
            r'Elapsed time \(parallel\): (\d+\.\d+) sec\.', last_line)
        if match:
            time_taken = match.group(1)
        else:
            time_taken = None

        # Создаем словарь с данными для строки DataFrame
        row_data[f'T{flag.replace("1-", "")}'] = time_taken

    # Добавляем словарь в список
    data.append(row_data)

# Создаем DataFrame из списка словарей
results_df = pd.DataFrame(data)

# Переиндексируем DataFrame по столбцу 'Size'
results_df.set_index('Size', inplace=True)

# Записываем DataFrame в CSV-файл
results_df.to_csv('results.csv')

print("Результаты успешно записаны в файл results.csv")
