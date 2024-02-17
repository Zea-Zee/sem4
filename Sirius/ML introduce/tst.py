import pandas as pd

example_1_columns = ['A', 'B']
example_1_data = [
    ['a', 3],
    ['aa', 5],
    ['aaa', 8],
    ['aa', 13]
]
example_1_table = pd.DataFrame(columns=example_1_columns, data=example_1_data)
example_1_factors = ['A']
print("ok")
