maze = [
    "#####",
    "#A B#",
    "#####"
]

for i, row in enumerate(maze):
   # print(i,row)
    for j,col in enumerate(row):
       # print(j,col)
        print(f"({i},{j}), {col}")