import numpy as np

trees = np.genfromtxt("puzzle_input.txt", delimiter=1, dtype=int)

tallest_trees = 0
current_best_scenic = 0

max_tree_rows = trees.shape[0] - 1
max_tree_cols = trees.shape[1] - 1

## part 2 only
def find_tree_distance(tree: int, other_trees: np.array) -> int:
    scenic_score = 0
    this_tree = tree

    for tree in other_trees:
        scenic_score += 1
        if this_tree > tree:
            continue
        else:
            break
    return scenic_score


## Not my proudest code... preeeetty sure this is inefficient but I have a
## hazy head today

for rdix, val in enumerate(trees):
    for cid, cval in enumerate(val):
        if rdix == 0 or cid == 0 or rdix == max_tree_rows or cid == max_tree_cols:
            tallest_trees += 1
        else:
            this_tree = trees[rdix, cid]

            left_trees = trees[rdix, 0:cid]
            top_trees = trees[0:rdix, cid]
            right_trees = trees[rdix, cid + 1 :]
            bottom_trees = trees[rdix + 1 :, cid]

            is_highest_left = np.all(this_tree > left_trees)
            is_highest_right = np.all(this_tree > right_trees)
            is_highest_top = np.all(this_tree > top_trees)
            is_highest_bottom = np.all(this_tree > bottom_trees)

            ## Flip the left and top tree array because we'll evaluate from
            ## nearest to furthest tree
            left_distance = find_tree_distance(this_tree, np.flip(left_trees))
            top_distance = find_tree_distance(this_tree, np.flip(top_trees))
            right_distance = find_tree_distance(this_tree, right_trees)
            bottom_distance = find_tree_distance(this_tree, bottom_trees)

            if (
                is_highest_bottom
                or is_highest_left
                or is_highest_right
                or is_highest_top
            ):
                tallest_trees += 1

            this_scenic = (
                left_distance * right_distance * top_distance * bottom_distance
            )

            if this_scenic > current_best_scenic:
                current_best_scenic = this_scenic


print(f"Part 1 answer is: {tallest_trees}")
print(f"Part 2 answer is: {current_best_scenic}")
