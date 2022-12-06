with open("puzzle_input.txt", "r") as lines:
    buffer = lines.readline().rstrip() ## a single string


initial_pos = 0
end_pos = 4

def check_unique(str: str) -> bool:
  for i in range(len(str)):
    for j in range(i + 1,len(str)):
      if(str[i] == str[j]):
        return False
  return True


def find_first_position(datastream:str, packet_size: int = 4) -> int:

    initial_pos = 0
    end_pos = packet_size

    while(end_pos < len(datastream)):
        candidate_seq = datastream[initial_pos: end_pos]

        if check_unique(candidate_seq):
            break
        else:
            end_pos +=1
            initial_pos +=1
    
    return end_pos

print(f"Part 1 answer is {find_first_position(buffer, 4)}")
print(f"Part 2 answer is {find_first_position(buffer, 14)}")
