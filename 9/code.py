with open("puzzle_input.txt", "r") as fil:
    moves = [mov.rstrip() for mov in fil.readlines()]

move_knot = {
    "R": lambda row, col: (row + 1, col),
    "L": lambda row, col: (row - 1, col),
    "U": lambda row, col: (row, col + 1),
    "D": lambda row, col: (row, col - 1),
}

## the rope has 10 knots. We are going to use the code from part 2 to solve
## part 1. It's just a generalization
knots = 10
rope = [(0, 0) for knot in range(0, knots)]
knot_movements = [set() for knot in range(0, knots)]

for move in moves:
    print(move)
    move = move.split(" ")
    direction = move[0]
    steps = int(move[1])

    for _ in range(steps):
        for kid, kpos in enumerate(rope):
            if kid == 0:  ## the head!!!!
                # Unpack row, col, less typing. Identical to rope[kid][0] and
                # rope[kid][1]
                rope[kid] = move_knot[direction](*rope[kid])
                knot_movements[kid].add(rope[kid])  ## not further ado for the head
            else:  ## not the head, but one of the subsequent knots
                prev_knot = rope[kid - 1]
                delta_row = prev_knot[0] - kpos[0]
                delta_col = prev_knot[1] - kpos[1]

                ## Illegal position
                if abs(delta_row) > 1 or abs(delta_col) > 1:

                    ## Taking this shorcut from a reddit user. It removes
                    ## a lot of boiler plate code about diagonals. Basically,
                    ##  this will return either +1 or -1 cuz. 0 division will
                    ## be performed by 1 instead
                    delta_row //= abs(delta_row or 1)
                    delta_col //= abs(delta_col or 1)

                    rope[kid] = (kpos[0] + delta_row, kpos[1] + delta_col)

                knot_movements[kid].add(rope[kid])

## Part 1 only considers two knots
print(f"Part 1 answer is {len(knot_movements[1])}")
## Part 2 asks for the last knot
print(f"Part 2 answer is {len(knot_movements[knots - 1])}")
