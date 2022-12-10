with open("puzzle_input.txt", "r") as fil:
    stack = [line.rstrip() for line in fil.readlines()]

x = 1
register = [x]

for cmd in stack:
    if cmd == "noop":
        register.append(x)
    else:
        register.append(x)
        val = int(cmd.split(" ")[1])
        x += val
        register.append(x)

part1 = 0
for ctick in [20, 60, 100, 140, 180, 220]:
    part1 = part1 + ctick * register[ctick - 1]

print(f"part 1 answer is {answer_1}")

## This is a  glorious CRT T.T
hmax = 40
CRT = []

for tick, val in enumerate(register):
    ## the X register is the central sprite pos
    if abs(val - (tick % hmax)) <= 1:  
        CRT.append("#")
    else:
        CRT.append(".")

print("Part 2 answer is:")
for i in range(0, len(register) // hmax):
    print("".join(CRT[i * hmax : (i + 1) * hmax]))
