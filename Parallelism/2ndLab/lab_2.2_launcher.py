import subprocess
import pandas as pd
import re


cpu_flags = ['1-2', '1-4']#, '1-8', '12', '1-16',
             #'1-20', '1-24', '1-28', '1-32', '1-36', '1-40', '1-80']


data = []
for flag in cpu_flags:
    command = f"taskset -c {flag} ./integral"
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)

    output_lines = result.stdout.splitlines()
    last_line = output_lines[-1]
    match = re.search(
        r'Speedup: (\d+\.\d+)', last_line)
    if match:
        time_taken = match.group(1)
    else:
        time_taken = None
    print(time_taken)
# data.append(row_data)


# results_df = pd.DataFrame(data)
# results_df.set_index('Size', inplace=True)
# results_df.to_csv('results.csv')
# print("Результаты успешно записаны в файл results.csv")
