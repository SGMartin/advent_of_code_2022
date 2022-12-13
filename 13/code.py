from collections import defaultdict
from random import choice

with open("puzzle_input.txt", "r") as fil:
    raw_packets = [packet.rstrip() for packet in fil.readlines() if packet != "\n"]


## Ugliest code ever but hey, it will parse the packet (string) as code
## to convert the pseudo-code lists to actual lists
def build_packet(code):
    exec("global i; i = %s" % code)
    global i
    return i


def sort_inorder_integer(i, j):
    if i == j:
        return 0
    else:
        status = -1 if i < j else 1
        return status


def sort_inorder_list(l1, l2):
    status = 0

    for el1, el2 in zip(l1, l2):
        ## Check that we don't have nested lists
        el1_type = "int" if isinstance(el1, int) else "list"
        el2_type = "int" if isinstance(el2, int) else "list"

        if el1_type == el2_type and el1_type == "int":
            status = sort_inorder_integer(el1, el2)
        else:
            el1 = [el1] if el1_type == "int" else el1
            el2 = [el2] if el2_type == "int" else el2
            status = sort_inorder_list(el1, el2)

        if status != 0:
            return status

    if abs(len(l1) - len(l2)) > 0:
        status = -1 if len(l1) < len(l2) else 1

    return status


# TODO: move some of this to the recursive func.
# For instance, the list/check comp


def sort_pairs(p1, p2):
    status = 0
    for el1, el2 in zip(p1, p2):
        el1_type = "int" if isinstance(el1, int) else "list"
        el2_type = "int" if isinstance(el2, int) else "list"

        if el1_type == el2_type and el1_type == "int":
            status = sort_inorder_integer(el1, el2)
        else:
            el1 = [el1] if el1_type == "int" else el1
            el2 = [el2] if el2_type == "int" else el2
            status = sort_inorder_list(el1, el2)  ## recursive call

        if status != 0:
            break

    if status == 0:
        if len(p1) < len(p2):
            status = -1
        else:
            status = 1

    return status


### stackoverflow: https://stackoverflow.com/questions/913624/sorting-algorithm-where-pairwise-comparison-can-return-more-information-than-1
def quicksort(seq, compare):
    "Stable in-place sort using a 3-or-more-way comparison function"
    # Make an n-way partition on a random pivot value
    segments = defaultdict(list)
    pivot = choice(seq)
    for x in seq:
        ranking = 0 if x is pivot else compare(x, pivot)
        segments[ranking].append(x)
    seq.clear()
    # Recursively sort each segment and store it in the sequence
    for ranking, segment in sorted(segments.items()):
        if ranking and len(segment) > 1:
            quicksort(segment, compare)
        seq += segment


all_packets = [build_packet(packet) for packet in raw_packets if packet]

## Split the list in two lists: packet1 packet 3 and packet0, packet 2 for ex.
pairs_of_packets = zip(all_packets[0::2], all_packets[1::2])

sorted_pairs_idx = []
sorted_pairs_stack = []

for pid, (p1, p2) in enumerate(pairs_of_packets):
    sort_status = sort_pairs(p1, p2)
    if sort_status == -1:
        sorted_pairs_idx.append(pid + 1)
        sorted_pairs_stack.extend([p1, p2])
    else:
        sorted_pairs_stack.extend([p2, p1])


print(f"Part 1 answer is: {sum(sorted_pairs_idx)}")

# For part 2, we have to insert two new packets
## Pairs are already sorted, but now we need an absolute hierarchy
## and not pair sorting

all_packets.append([[2]])
all_packets.append([[6]])

quicksort(all_packets, sort_pairs)

decoder_1, decoder_2 = 0, 0

for pid, packet in enumerate(all_packets):

    if packet == [[2]]:
        decoder_1 = pid + 1

    if packet == [[6]]:
        decoder_2 = pid + 1


print(f"Part 2 answer is {decoder_1 * decoder_2}")
