with open("puzzle_input.txt", "r") as fil:
    pairs = [pair.rstrip() for pair in fil.readlines()]

full_match = 0
overlaps = 0

for pair in pairs:
    sub_pairs = pair.split(",")

    sub0 = sub_pairs[0].split("-")
    sub1 = sub_pairs[1].split("-")

    sub0 = range(int(sub0[0]), int(sub0[1]) + 1)
    sub1 = range(int(sub1[0]), int(sub1[1]) + 1)

    sub0 = set(sub0)
    sub1 = set(sub1)

    if sub0.issubset(sub1) or sub1.issubset(sub0):
        full_match = full_match + 1

    if sub0.intersection(sub1):
        overlaps += 1


print(f"Answer to P1 is {full_match}")
print(f"Answer to P2 is {overlaps}")
