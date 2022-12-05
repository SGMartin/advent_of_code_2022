import copy
import re

## NOTE: most of the solutions I've seen manually code the stacks
## I refuse to follow any kind of approach like that so let the parsing begin

## scan n. of crates. The previous lines will be the crate
## arrangement
stacked_crates = 0
crane_orders = []
crate_numbering = []
crate_lines = []


def crane_crates(crate_stack: list, crane_cmd: list, from_top: bool = True) -> list:
    # position 0 -> crates to move
    # position 1 -> origin
    # position 2 -> new crate columns
    new_stack = crate_stack
    n_crates = int(crane_cmd[0])
    old_col = int(crane_cmd[1])
    new_col = int(crane_cmd[2])

    crates_to_move = new_stack[old_col][-n_crates:]
    if from_top:
        crates_to_move.reverse()
    
    new_stack[new_col].extend(crates_to_move)
    new_stack[old_col] = new_stack[old_col][:len(new_stack[old_col]) - n_crates]

    return new_stack


## We'll split the input in three parts: 
# a) Find the crate column numbering
# b) Find the crane orders
# c) The top of the file, the crate columns themselves

with open("puzzle_input.txt", "r") as fil:
   
   for idx, line in enumerate(fil.readlines()):
        if line.startswith(" 1"):
            col_array = [x for x in line.rstrip().split(" ")]
            col_array = [int(x) for x in col_array if x != ""]
            stacked_crates = max(col_array)
            crate_numbering = [line.rstrip().index(str(x)) for x in col_array]
            continue
        if line.startswith("move"):
            crane_orders.append(line.rstrip())
            continue
        if line.rstrip() != "":
            crate_lines.append(line.rstrip())


crates = {k:[] for k in range(1, stacked_crates + 1)}
crate_char_pos = dict(zip(range(1, stacked_crates + 1), crate_numbering))

for crate_line in crate_lines:
    for crate, pos in crate_char_pos.items():
        if len(crate_line) >= pos:
            if crate_line[pos] != " ":
                crates[crate].append(crate_line[pos])


for key,val in crates.items():
    crates[key].reverse()

## We'll need a copy for part two
crates_reordered = copy.deepcopy(crates)

for crane_order in crane_orders:
    orders = re.findall(r'\d+', crane_order)
    crates_reordered = crane_crates(crates_reordered, orders, from_top=True)
    
last_crates = []
for crate_id, crate_col in crates_reordered.items():
    last_crates.append(crates_reordered[crate_id].pop())

last_crates = "".join(last_crates)
print(f"Part 1 answer is: {last_crates}")

## Part 2
for crane_order in crane_orders:
    orders = re.findall(r'\d+', crane_order)
    crates = crane_crates(crates, orders, from_top=False) # this is the only dif. 

last_crates_part2 = []
for crate_id, crate_col in crates.items():
    last_crates_part2.append(crates[crate_id].pop())

last_crates_part2 = "".join(last_crates_part2)
print(f"Part 2 answer is: {last_crates_part2}")
