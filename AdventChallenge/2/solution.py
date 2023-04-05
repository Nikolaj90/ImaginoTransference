import pandas as pd

df_main = pd.read_csv("input.csv", delimiter = " ", header = None)

df1 = df_main.copy()

# Crating a dict of dicts, input is my choice, then the elfs and the output 
# should be D for draw, W for won or L for lost
result = {"X": {"A":"D", "B": "L", "C":"W"},
         "Y": {"A":"W", "B": "D", "C":"L"},
         "Z": {"A":"L", "B": "W", "C":"D"}}

df1["result"] = [result[row[1]][row[0]] for i, row in df1.iterrows()]

# Points for result
point_result = {"W": 6, "D": 3, "L":0}
# Points for shape
point_shape = {"X":1, "Y":2, "Z":3}

df1["Point_result"] = [point_result[result] for result in df1["result"]]
df1["Point_shape"] = [point_shape[shape] for shape in df1[1]]

# What is the total score!
print(df1["Point_result"].sum() + df1["Point_shape"].sum())

# ### Part 2 

df2 = df_main.copy()

# Determine what the result should be
result2 = {"X": "L", "Y" : "D", "Z" : "W"}
df2["result"] = [result2[result] for result in df2[1]]

# What is the opponents move
# What is the countermove to achieve the result
myShape = {"L": {"A":"Z", "B": "X", "C":"Y"}, # lose
         "D": {"A":"X", "B": "Y", "C":"Z"}, # draw
         "W": {"A":"Y", "B": "Z", "C":"X"}} # win
df2["shape"] = [myShape[row["result"]][row[0]] for i, row in df2.iterrows()]

# Calculate points
df2["Point_result"] = [point_result[result] for result in df2["result"]]
df2["Point_shape"] = [point_shape[shape] for shape in df2["shape"]]

# Total score
print(df2["Point_result"].sum() + df2["Point_shape"].sum())

