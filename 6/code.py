with open("puzzle_input.txt", "r") as lines:
    buffer = lines.readline().rstrip()  ## a single string

initial_pos = 0
end_pos = 4


def find_first_position(datastream: str, packet_size: int = 4) -> int:

    initial_pos = 0
    end_pos = packet_size

    while end_pos < len(datastream):
        candidate_seq = datastream[initial_pos:end_pos]

        if len(set(candidate_seq)) == packet_size:
            break
        else:
            end_pos += 1
            initial_pos += 1

    return end_pos


print(f"Part 1 answer is {find_first_position(buffer, 4)}")
print(f"Part 2 answer is {find_first_position(buffer, 14)}")
