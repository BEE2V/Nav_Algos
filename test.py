lab = ["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
       "🟦❎🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦🟦🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦❎🟦🟦🟦❎🟦❎🟦",
       "🟦❎❎❎🟦❎🟦❎🟦🟥🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦🟨🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]

seen_labyrinth = [
    [cell if (i == 0 or i == len(lab) - 1 or j == 0 or j == len(row) - 1) else "🟩"
     for j, cell in enumerate(row)]
    for i, row in enumerate(lab)
]

# for row in seen_labyrinth:
    # print("".join(row))

print(seen_labyrinth)