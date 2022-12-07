from collections import defaultdict

TOTAL_DISK_SPACE = 70000000
NEED_TO_ALLOCATE = 30000000
PART1_RANDOM_CONDITION = 100000

all_tree_sizes = defaultdict(int)
path = []


def build_path(cur_path: list, this_dir: str) -> str:
    previous_level = cur_path[-1]
    new_sub_path = "/" if previous_level != "/" else ""
    new_path = f"{previous_level}{new_sub_path}{directory}"
    return new_path


with open("puzzle_input.txt", "r") as fil:
    prompt = [line.rstrip() for line in fil.readlines()]

for line in prompt:
    if line.startswith("$ cd"):
        directory = line.split()[2]  ## $ cd /<dir>
        if directory == "/":  ## tree root
            path.append("/")
        elif directory == "..":  ## Go UP!
            path.pop()
        else:
            this_new_path = build_path(path, directory)
            path.append(this_new_path)
    if line[0].isnumeric():  ## files start with the size first
        for p in path:
            file_size = int(line.split()[0])
            all_tree_sizes[p] += file_size

part1_answer = sum(s for s in all_tree_sizes.values() if s <= PART1_RANDOM_CONDITION)
part2_answer = min(
    s
    for s in all_tree_sizes.values()
    if s >= NEED_TO_ALLOCATE - (TOTAL_DISK_SPACE - all_tree_sizes["/"])
)

print(f"Part 1 answer is: {part1_answer}")
print(f"Part 2 answer is: {part2_answer}")
