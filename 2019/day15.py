#!/usr/local/bin/python3.7

import Intcode
import os

class Grid:
	grid = {'0,0': 1}
	closed = []
	x, y = 0, 0
	x_range = [0, 0]
	y_range = [0, 0]
	goal = [0, 0]

	def __init__(self):
		self.grid = {'0,0': 1}
		self.x = 0
		self.y = 0

	def get_tile(self, x, y):
		if f"{x},{y}" in self.grid:
			return self.grid[f"{x},{y}"]
		else:
			return None

	''' Based on the current grid, provide the next move '''
	def next_move(self):
		# Move into unexplored spaces first. Move priority: U, R, D, L
		if f"{self.x},{self.y + 1}" not in self.grid:
			return 1
		elif f"{self.x + 1},{self.y}" not in self.grid:
			return 4
		elif f"{self.x},{self.y - 1}" not in self.grid:
			return 2
		elif f"{self.x - 1},{self.y}" not in self.grid:
			return 3

		# If there are no adjacent unexplored spaces, try moving out of the explored space
		# Adds the current space into the closed set to organically close off dead-ends.
		self.closed.append(f"{self.x},{self.y}")
		if self.grid[f"{self.x},{self.y + 1}"] != 0 and f"{self.x},{self.y + 1}" not in self.closed:
			return 1
		elif self.grid[f"{self.x + 1},{self.y}"] != 0 and f"{self.x + 1},{self.y}" not in self.closed:
			return 4
		elif self.grid[f"{self.x},{self.y - 1}"] != 0 and f"{self.x},{self.y - 1}" not in self.closed:
			return 2
		elif self.grid[f"{self.x - 1},{self.y}"] != 0 and f"{self.x - 1},{self.y}" not in self.closed:
			return 3

	''' Based on the attempted direction and result from the VM, update the grid and current position '''
	def move(self, direct, result):
		if direct == 1:
			self.grid[f"{self.x},{self.y + 1}"] = result
			if self.y + 1 > self.y_range[1]:
				self.y_range[1] = self.y + 1

		elif direct == 2:
			self.grid[f"{self.x},{self.y - 1}"] = result
			if self.y - 1 < self.y_range[0]:
				self.y_range[0] = self.y - 1

		elif direct == 3:
			self.grid[f"{self.x - 1},{self.y}"] = result
			if self.x - 1 < self.x_range[0]:
				self.x_range[0] = self.x - 1

		elif direct == 4:
			self.grid[f"{self.x + 1},{self.y}"] = result
			if self.x + 1 > self.x_range[1]:
				self.x_range[1] = self.x + 1

		if result != 0:
			if direct == 1:
				self.y += 1
			elif direct == 2:
				self.y -= 1
			elif direct == 3:
				self.x -= 1
			elif direct == 4:
				self.x += 1

		if result == 2:
			self.goal = [self.x, self.y]

	''' Displays the current map in STDOUT '''
	def print_map(self):
		for y in range(self.y_range[1], self.y_range[0] - 1, -1):
			for x in range(self.x_range[0], self.x_range[1] + 1):
				if x == self.x and y == self.y:
					print("@", end="")
				elif x == 0 and y == 0:
					print("O", end="")
				elif f"{x},{y}" in self.grid:
					if self.grid[f"{x},{y}"] == 0:
						print("█", end="")
					elif self.grid[f"{x},{y}"] == 1:
						print(".", end="")
					elif self.grid[f"{x},{y}"] == 2:
						print("X", end="")
				else:
					print(" ", end="")
			print()

	''' Finds the shortest path to the oxygen system from start (0,0) via BFS '''
	def path_to_goal(self):
		openQ = [[0,0,'']]
		closed = []

		# BFS loop
		while len(openQ) > 0:
			# Pop the next node from the open queue
			current = openQ.pop(0)
			x = current[0]
			y = current[1]
			moves = current[2]

			# Check if this is the oxygen system's space. Return the current movelist, if so
			if x == self.goal[0] and y == self.goal[1]:
				return moves
			else:
				# Add all possible moves from this space to the open queue
				if f"{x+1},{y}" not in closed and f"{x+1},{y}" in self.grid and self.grid[f"{x+1},{y}"] != 0:
					openQ.append([x+1, y, moves + 'R'])

				if f"{x-1},{y}" not in closed and f"{x-1},{y}" in self.grid and self.grid[f"{x-1},{y}"] != 0:
					openQ.append([x-1, y, moves + 'L'])

				if f"{x},{y+1}" not in closed and f"{x},{y+1}" in self.grid and self.grid[f"{x},{y+1}"] != 0:
					openQ.append([x, y+1, moves + 'U'])

				if f"{x},{y-1}" not in closed and f"{x},{y-1}" in self.grid and self.grid[f"{x},{y-1}"] != 0:
					openQ.append([x, y-1, moves + 'D'])

				# Add the current space the closed set
				closed.append(f"{x},{y}")

		# Returns None if no valid path found
		return None

	''' Determine the time required to fill the entire maze with oxygen '''
	def oxygen_fill_time(self):
		open_space = list(self.grid.values()).count(1)
		closed = []
		openQ = [[self.goal[0], self.goal[1], 0]]

		while len(openQ) > 0 and len(closed) <= open_space:
			# Pop the next node from the open queue
			current = openQ.pop(0)
			x = current[0]
			y = current[1]
			time = current[2]

			# Add all possible new spaces to the open queue
			if f"{x+1},{y}" not in closed and f"{x+1},{y}" in self.grid and self.grid[f"{x+1},{y}"] != 0:
				openQ.append([x+1, y, time + 1])
			if f"{x-1},{y}" not in closed and f"{x-1},{y}" in self.grid and self.grid[f"{x-1},{y}"] != 0:
				openQ.append([x-1, y, time + 1])
			if f"{x},{y+1}" not in closed and f"{x},{y+1}" in self.grid and self.grid[f"{x},{y+1}"] != 0:
				openQ.append([x, y+1, time + 1])
			if f"{x},{y-1}" not in closed and f"{x},{y-1}" in self.grid and self.grid[f"{x},{y-1}"] != 0:
				openQ.append([x, y-1, time + 1])

			# Add the current space to the closed set
			closed.append(f"{x},{y}")

		# Returns the time taken to fill the entire maze.
		# Is also the maximum number of moves it takes to go to any space in the grid from the oxygen system
		return time

''' Given a pathlist, returns a version that condenses consective moves '''
def simplified_path(path):
	count = 1
	last_move = ''
	new_path = ''

	for move in path:
		if move == last_move:
			count += 1
		elif last_move != '':
			new_path += f"{count}{last_move}, "
			count = 1

		last_move = move

	if count != 1:
		new_path += f"{count}{last_move}, "

	return new_path[:-2]




def main():
	grid = Grid()
	VM = Intcode.VM("inputs/day15.txt", automated=True)
	running = True
	last_move = -1

	# Run the program until halted or until the entire map is discovered
	while running != False:
		running = VM.step()

		# Add the results from the latest move to the grid
		if VM.output_in_queue():
			grid.move( last_move, VM.read_from_output_queue() )
			#input('')

		# Check if the program is expecting input
		if running == None:
			# Determine the next move to take
			last_move = grid.next_move()
			
			# If there is a possible move, add it to the program's input queue
			if last_move != None:
				VM.add_to_input_queue( last_move )
				os.system('clear')
				grid.print_map()
			else:
				# If there are no possible moves, determine the challenge's questions
				os.system('clear')
				grid.print_map()
				path = grid.path_to_goal()
				print( simplified_path(path) )
				print( f"Moves from start to oxygen: {len(path)}" )
				print( f"Fill Time: { grid.oxygen_fill_time() } minutes")

				break

if __name__ == '__main__':
	main()
