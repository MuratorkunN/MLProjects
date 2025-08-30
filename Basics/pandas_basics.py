import pandas as pd

my_table = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

columns = ["col0", "col1", "col2"]
rows = ["row0", "row1", "row2"]

df = pd.DataFrame(my_table, columns=columns, index=rows)
print(df)

row0 =df.iloc[0]
print(row0)

row1 = df.loc["row1"]
print(row1)

col0 = df["col0"]
print(col0)

col01 = df[["col0", "col1"]]
print(col01)

element = df.iloc[1, 1]
print(element)
element = df.loc["row1", "col1"]
print(element)

df.loc["new_row"] = [0, 0, 0]
df["new_col"] = [0, 0, 0, 0]
print(df)

df = df.drop("new_col", axis = 1)
print(df)

