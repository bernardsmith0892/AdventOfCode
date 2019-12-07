import re

def turn_on(sx, sy, ex, ey, grid, version):
	for x in range(sx, ex + 1):
		for y in range(sy, ey + 1):
			if version == 1:
				grid[x][y] = 1
			else:
				grid[x][y] += 1

	return grid

def turn_off(sx, sy, ex, ey, grid, version):
	for x in range(sx, ex + 1):
		for y in range(sy, ey + 1):
			if version == 1:
				grid[x][y] = 0
			else:
				grid[x][y] -= 1 if grid[x][y] > 0 else 0

	return grid

def toggle(sx, sy, ex, ey, grid, version):
	for x in range(sx, ex + 1):
		for y in range(sy, ey + 1):
			if version == 1:
				grid[x][y] = 1 if grid[x][y] == 0 else 0
			else:
				grid[x][y] += 2

	return grid

def parse_command(cmd_str, grid, version):
	cmd_re = '([a-z ]+) (\d{1,3}),(\d{1,3}) through (\d{1,3}),(\d{1,3})'
	re_match = re.match(cmd_re, cmd_str)

	cmd = re_match.group(1)
	sx, sy = int(re_match.group(2)), int(re_match.group(3))
	ex, ey = int(re_match.group(4)), int(re_match.group(5))

	if cmd == "turn on":
		grid = turn_on(sx, sy, ex, ey, grid, version)
	elif cmd == "turn off":
		grid = turn_off(sx, sy, ex, ey, grid, version)
	elif cmd == "toggle":
		grid = toggle(sx, sy, ex, ey, grid, version)
	else:
		print("INVALID COMMAND! QUITTING...")
		exit()

	return grid

def print_grid(grid):
	for x in grid:
		for y in x:
			print(f'{"*" if y else " "}', end='')
		print()
	print()


def main(version):
	# grid = [[False] * 1000] * 1000 -- THIS DOESN'T WORK!! Each column is a reference to a single memory location, so it's not a 2d array at all.
	grid = [[0] * 1000 for i in range(1000)]	

	with open('inputs/day6.txt', 'r') as data:
			for cmd in data.readlines():
				grid = parse_command(cmd, grid, version)

	lights_on = 0
	for x in grid:
		for y in x:
			lights_on += y

	print(lights_on)

main(1)
main(2)