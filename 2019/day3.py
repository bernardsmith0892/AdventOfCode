#!/usr/local/bin/python3.7

def print_grid(grid):
	max_x = 0
	min_x = 0
	max_y = 0
	min_y = 0

	for i in grid.items():
		x = int(i[0].split(',')[0])
		y = int(i[0].split(',')[1])

		if x > max_x:
			max_x = x
		elif x < min_x:
			min_x = x

		if y > max_y:
			max_y = y
		elif y < min_y:
			min_y = y

	for y in range(max_y, min_y - 1, -1):
		for x in range(min_x, max_x + 1):
			if x == 0 and y == 0:
				print('O', end='')
			elif f"{x},{y}" not in grid:	
				print('.', end='')
			elif grid[f"{x},{y}"] == 1:
				print('*', end='')
			elif grid[f"{x},{y}"] > 1:
				print('X', end='')

		print('')

def place_wire(x, y, step, grid, first_wire):
	if first_wire:
		grid[f"{x},{y}"] = [step, 0]
	elif not first_wire:
		if f"{x},{y}" in grid:
			grid[f"{x},{y}"][1] = step
		else:
			grid[f"{x},{y}"] = [0, step]

def add_wire_length(cmd, x, y, step, grid, first_wire):
	direction = cmd[0]
	distance = int(cmd[1:])

	for i in range(distance):
		step += 1
		if direction == 'U':
			y += 1
		elif direction == 'D':
			y -= 1
		elif direction == 'R':
			x += 1
		elif direction == 'L':
			x -= 1
		else:
			print('UNEXPECTED COMMAND! QUITTING!')
			exit()

		place_wire(x, y, step, grid, first_wire)

	return x,y,step


def main():
	with open("inputs/day3.txt", "r") as data:
		wire_a = data.readline().split(',')
		wire_b = data.readline().split(',')

	grid = {}

	x,y,step = 0,0,0
	for cmd in wire_a:
		x,y,step = add_wire_length(cmd, x, y, step, grid, True)

	x,y,step = 0,0,0
	for cmd in wire_b:
		x,y,step = add_wire_length(cmd, x, y, step, grid, False)

	min_dist = -1
	for i in grid.items():
		x = abs(int(i[0].split(',')[0]))
		y = abs(int(i[0].split(',')[1]))
		steps_a = i[1][0];
		steps_b = i[1][1];

		if steps_a > 0 and steps_b > 0:
			#print(f"{i} - {steps_a + steps_b}")
			if (steps_a + steps_b) < min_dist or min_dist == -1:
				min_dist = steps_a + steps_b

	#print_grid(grid)
	print(len(grid))
	print(min_dist)

main()