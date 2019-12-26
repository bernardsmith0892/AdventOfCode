#!/usr/local/bin/python3.7

import Intcode
import os

def find_intersections(grid):
	intersections = []
	for y in range(1, len(grid) - 1):
		for x in range(1, len(grid[y]) - 1):
			if grid[y][x] == "#":
				if grid[y-1][x] == "#":
					if grid[y+1][x] == "#":
						if grid[y][x-1] == "#":
							if grid[y][x+1] == "#":
								intersections.append((x,y))
	print()
	return intersections

def print_grid(grid):
	for y in range(0, len(grid)):
		for x in range(0, len(grid[y])):
			print(grid[y][x], end="")
		print()

def path_to_all(grid, start, scaffolds):
	moves = ''
	x,y = start[0], start[1]
	direction = 'U'

	while True:
		# Prefer moving forward, but turn if required
		if direction == 'U':
			if y - 1 >= 0 and grid[y - 1][x] == '#':
				moves += 'F'
				y -= 1
			elif x - 1 >= 0 and grid[y][x - 1] == '#':
				moves += 'L'
				direction = 'L'
			elif x + 1 < len(grid[y]) and grid[y][x + 1] == '#':
				moves += 'R'
				direction = 'R'
			else:
				return moves
		elif direction == 'D':
			if y + 1 < len(grid) and grid[y + 1][x] == '#':
				moves += 'F'
				y += 1
			elif x - 1 >= 0 and grid[y][x - 1] == '#':
				moves += 'R'
				direction = 'L'
			elif x + 1 < len(grid[y]) and grid[y][x + 1] == '#':
				moves += 'L'
				direction = 'R'
			else:
				return moves
		elif direction == 'L':
			if x - 1 >= 0 and grid[y][x - 1] == '#':
				moves += 'F'
				x -= 1
			elif y - 1 >= 0 and grid[y - 1][x] == '#':
				moves += 'R'
				direction = 'U'
			elif y + 1 < len(grid) and grid[y + 1][x] == '#':
				moves += 'L'
				direction = 'D'
			else:
				return moves
		elif direction == 'R':
			if x + 1 < len(grid[y]) and grid[y][x + 1] == '#':
				moves += 'F'
				x += 1
			elif y - 1 >= 0 and grid[y - 1][x] == '#':
				moves += 'L'
				direction = 'U'
			elif y + 1 < len(grid) and grid[y + 1][x] == '#':
				moves += 'R'
				direction = 'D'
			else:
				return moves

def compile_path(path):
	clean_path = ""
	forward_count = 0
	for c in path:
		if c != 'F':
			if forward_count > 0:
				clean_path += f"{forward_count},"
				forward_count = 0
			clean_path += f"{c},"
		if c == 'F':
			forward_count += 1

	if forward_count > 0:
				clean_path += f"{forward_count},"

	return clean_path[:-1]

def convert_to_decimal(string):
	chars = []
	for c in string:
		chars.append( ord(c) )

	return chars



def main():
	VM = Intcode.VM("inputs/day17.txt", automated=True)
	running = True
	
	# Part 1
	x,y = 0,0
	scaffolds = 0
	start = [0,0]
	grid = []
	line = []
	while running != False:
		running = VM.step()

		if VM.output_in_queue():
			output = chr( VM.read_from_output_queue() )
			if output != '\n':
				line.append(output)
				if output == '^':
					start = [x, y]
				elif output == '#':
					scaffolds += 1
				x += 1
			else:
				grid.append(line)
				y += 1
				line = []

	grid = grid[:-1]
	print_grid(grid)
	intersections = find_intersections(grid)
	print(intersections)

	align_params = 0
	for i in intersections:
		align_params += i[0] * i[1]

	print(f"Sum of Alignment Parameters: {align_params}")
	print(f"Start: {start}, Scaffolds: {scaffolds}")

	# Part 2
	path = path_to_all(grid, start, scaffolds)
	print(compile_path(path))

	# The analysis on how to organize movement commands was performed manually
	A = 'L,12,L,12,R,4\n'
	B = 'R,10,R,6,R,4,R,4\n'
	C = 'R,6,L,12,L,12\n'
	Main = 'A,B,A,C,B,A,B,C,C,B\n'

	A = convert_to_decimal(A)
	B = convert_to_decimal(B)
	C = convert_to_decimal(C)
	Main = convert_to_decimal(Main)

	VM = Intcode.VM("inputs/day17.txt", automated=True)
	VM.poke(0, 2)
	running = True

	while running != False:
		running = VM.step()

		if VM.output_in_queue():
			output = chr( VM.read_from_output_queue() )
			if ord(output) <= 255:
				print(output, end="")
			else:
				print(ord(output))

		if running == None:
			for c in Main:
				VM.add_to_input_queue(c)
			for c in A:
				VM.add_to_input_queue(c)
			for c in B:
				VM.add_to_input_queue(c)
			for c in C:
				VM.add_to_input_queue(c)
			VM.add_to_input_queue(ord('n'))


if __name__ == "__main__":
	main()