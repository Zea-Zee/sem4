import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import re

# import seaborn as sns


def build_plot(df):
    indices = [int(col) for col in df.columns]
    values = [float(val) for val in df.iloc[0].values]

    plt.figure(figsize=(10, 10))
    plt.title("Speedup dependency from threads")

    plt.plot(indices, values, marker="o", label="Speedup")
    plt.plot(indices, indices, linestyle="--", color="red", label="y=x")

    plt.xticks(indices)
    plt.yticks(values)

    plt.xlabel("T num")
    plt.ylabel("Speedup")

    plt.grid(True)
    plt.legend()
    plt.savefig("lab2_2.png")
    plt.close()


cpu_flags = [
    "1-2",
    "1-4",
    "1-8",
    "1-12",
    "1-16",
    "1-20",
    "1-24",
    "1-28",
    "1-32",
    "1-36",
    "1-40",
    "1-44",
    "1-48",
    "1-52",
    "1-56",
    "1-60",
    "1-64",
    "1-68",
    "1-72",
    "1-76",
    "1-80",
]

# cpu_flags = ['1-2', '1-32', '1-36', '1-40', '1-60', '1-80']
# cpu_flags = ['1-2', '1-4', '1-8', '1-12']
# cpu_flags = ['1-8', '1-12']


subprocess.run("./integral", shell=True, capture_output=True, text=True)


data = {}
data["1"] = [1]
for flag in cpu_flags:
    command = f"taskset -c {flag} ./integral -parallel"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output_lines = result.stdout.splitlines()
    last_line = output_lines[-1]
    match = re.search(r"Speedup: (\d+\.\d+)", last_line)
    speedup = match.group(1)
    data[int(flag.split("-")[1])] = [float(speedup)]
print(data)

results_df = pd.DataFrame(data)
build_plot(results_df)
