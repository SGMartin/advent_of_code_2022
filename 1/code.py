## Generate a list of list where each list is an elf cal.count
with open("puzzle_input.txt", "r") as cals:
    all_lines = (
        cals.read().rstrip()
    )  ## Get rid of final new line if I managed to copy it
    elfs = [line.split("\n") for line in all_lines.split("\n\n")]

## Cast to int each elf cals. and sum them to get a list of total cals/elf
all_elfs = [sum(map(int, elf_cals)) for elf_cals in elfs]


print(f"Day 1/1 answer is: {sorted(all_elfs, reverse=True)[0]} calories")
print(f"Day 1/2 answer is: {sum(sorted(all_elfs, reverse=True)[0:3])} calories")
