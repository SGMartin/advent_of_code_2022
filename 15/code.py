import re 

def parse_sensor_beacon(line: str):
    parser = (r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    beacon_parser = re.compile(parser)
    results = beacon_parser.match(line)
    
    return results

def manhattan_dist(a, b):
    return sum(abs(x0-x1) for x0, x1 in zip(a,b))

with open("puzzle_input.txt", "r") as fil:
    beacon_sensors = [line.rstrip() for line in fil.readlines()]

sensors = {}
max_x, max_y, min_x, min_y = 0,0,0,0 

for line in beacon_sensors:
    matched = parse_sensor_beacon(line)

    x0, y0, x1, y1 = int(matched[1]), int(matched[2]), int(matched[3]), int(matched[4])
    sensors[(x0, y0)] = (x1, y1)

    ##TODO: Refactor this
    if max([x0, x1]) > max_x:
        max_x = max([x0, x1])
    
    if max([y0, y1]) > max_y:
        max_y = max([y0, y1])

    if min([x0, x1]) < min_x:
        min_x = min([x0, x1])
    
    if min([y0, y1]) < min_y:
        min_y = min([y0, y1])

## A dictionary of sensors and manhattan distances to the closest beacon
beacon_dists = {sensor: manhattan_dist(sensor, value) for sensor, value in sensors.items()}
beacon_range = {sensor: (range(sensor[0] - distance, sensor[0] + distance + 1), range(sensor[1] - distance, sensor[1] + distance + 1)) for sensor, distance in beacon_dists.items()}

# random row, independent of actual pos. It is a rectangular grid after all

## HERE THERE IS A FAILURE LOL. IF ROW 2000.000 then the grid is much HIGHER
row_range = set(list(range(min_x, max_x + 1)))
target_row = 2000000
print(len(row_range))

print(min_x, max_x, min_y, max_y)
scaned_sets = set()
for sensor, area in beacon_range.items():
    if target_row in area[0]:
        ## the amount of overlapped slots is (x, area1)
        all_idx = set(list(area[1]))
        overlap = all_idx.intersection(row_range)
        scaned_sets.update(overlap)

## scanned_set contains all the potential positions, but it also may include
## beacons or sensors. We have to remove them if they are in the way.
for sensor, beacon in sensors.items():
    if sensor[1] == target_row and sensor[0] in scaned_sets:
        scaned_sets.remove(sensor[0])
    if beacon[1] == target_row and beacon[0] in scaned_sets:
        scaned_sets.remove(beacon[0])

#print(scaned_sets)
print(len(scaned_sets))
