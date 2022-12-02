with open("puzzle_input.txt", "r") as fil:
    games = [game.strip().replace(" ", "") for game in fil.readlines()]


## there are only 9 pos. combs.
strat_first_meaning = {    
    "AX": 4,
    "AY": 8,
    "AZ": 3,
    "BX": 1,
    "BY": 5,
    "BZ": 9,
    "CX": 7,
    "CY": 2,
    "CZ": 6
    }

strat_second_meaning = {
    "AX": 3,
    "AY": 4,
    "AZ": 8,
    "BX": 1, 
    "BY": 5,
    "BZ": 9,
    "CX": 2,
    "CY": 6,
    "CZ": 7
    }

first_meaning_scores = [strat_first_meaning[game] for game in games]
second_meaning_scores = [strat_second_meaning[game] for game in games]

print(f"Answer to part 1 is: {sum(first_meaning_scores)}")
print(f"Answer to part 2 is: {sum(second_meaning_scores)}")
