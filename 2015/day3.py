#!/usr/local/bin/python3.7

def move(x, y, direction):
	if direction == '^':
		y += 1
	elif direction == 'v':
		y -= 1
	elif direction == '>':
		x += 1
	elif direction == '<':
		x -= 1

	return x, y

def part1():
	x, y = 0, 0
	houses = {}
	houses[f"{x},{y}"] = 1

	with open("inputs/day3.txt", "r") as directions:
		for d in directions.readline():
			x, y = move(x, y, d)
			if f"{x},{y}" in houses:
				houses[f"{x},{y}"] += 1
			else:
				houses[f"{x},{y}"] = 1

	print(len(houses))

def part2():
	robo_move = False
	x, y = 0, 0
	i, j = 0, 0
	houses = {}
	houses[f"{x},{y}"] = 2
	
	with open("inputs/day3.txt", "r") as directions:
		for d in directions.readline():
			if not robo_move:
				x, y = move(x, y, d)
				if f"{x},{y}" in houses:
					houses[f"{x},{y}"] += 1
				else:
					houses[f"{x},{y}"] = 1
			else:
				i, j = move(i, j, d)
				if f"{i},{j}" in houses:
					houses[f"{i},{j}"] += 1
				else:
					houses[f"{i},{j}"] = 1

			robo_move = not robo_move

	print(len(houses))

part1()
part2()