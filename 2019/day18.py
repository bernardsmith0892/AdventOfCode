#!/usr/local/bin/python3.7

from collections import namedtuple, deque, defaultdict
import queue
import time

class Coord:
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

class State:
	node = ''
	inv = ''
	path = ''

	def __init__(self, name, inv, path):
		self.name = name
		self.inv = inv
		self.path = path

	def __str__(self):
		return f"{self.name}, {''.join(self.inv)}, {self.path}"

	def __repr__(self):
		return {'name': self.name, 'inv': self.inv, 'steps': self.steps}

class Vertex:
	end = ''
	key = ''
	length = 0

	def __init__(self, end, length):
		self.end = end
		self.length = length

		if self.end in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			self.key = self.end.lower()
		else:
			self.key = ''

	def is_traversable(self, inv):
		return self.key == '' or inv[ord(self.key) - 97] != '.'


def is_traversable(tile, inv):
	if tile == '#':
		return False
	elif tile in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
		o = ord(tile.lower())
		return inv[o - 97] != '.'
	else:
		return True

def is_not_closed(pos, inv, closed):
	return f"{pos},{inv}" not in closed

def sort_keys(key):
	key = list(key)
	key.sort()
	return "".join(key)

def add_new_keys(keys, inv):
	new_inv = inv
	for k in keys:
		if k not in inv:
			new_inv += k

	return new_inv

def generate_graph(grid):
	closed = {}
	nodes = {}
	openQ = []

	# Determine starting positions
	for y in range( len(grid) ):
		for x in range( len(grid[y]) ):
			# Add all non-wall and non-empty tiles to openQ and list of nodes
			if grid[y][x] != '#' and grid[y][x] != '.':
				openQ.append([grid[y][x], Coord(x, y), 0])
				nodes[grid[y][x]] = []

	# Generate graphs
	while len(openQ) > 0:
		print(f"  Open: {len(openQ)}, Closed: {len(closed)}      ", end="\r")
		current = openQ.pop(0)
		node = current[0]
		pos = current[1]
		steps = current[2]

		# Add to closed list
		if node in closed:
			closed[node].append(f"{pos.x},{pos.y}")
		else:
			closed[node] = [f"{pos.x},{pos.y}"]

		# If this is a non-wall or non-empty tile, connect it with the current node and stop
		if grid[pos.y][pos.x] != node and grid[pos.y][pos.x] != '#' and grid[pos.y][pos.x] != '.':
			if node in nodes:
				nodes[node].append( Vertex(grid[pos.y][pos.x], steps) )
			else:
				nodes[node] = [ Vertex(grid[pos.y][pos.x], steps) ]

		# Otherwise, add all adjacent non-wall nodes
		else:
			# Up
			if pos.y > 0 and f"{pos.x},{pos.y - 1}" not in closed[node] and grid[pos.y - 1][pos.x] != '#':
					openQ.append( [node, Coord(pos.x, pos.y - 1), steps + 1] )
			# Down
			if pos.y < (len(grid) - 1) and f"{pos.x},{pos.y + 1}" not in closed[node] and grid[pos.y + 1][pos.x] != '#':
					openQ.append( [node, Coord(pos.x, pos.y + 1), steps + 1] )
			# Left
			if pos.x > 0 and f"{pos.x - 1},{pos.y}" not in closed[node] and grid[pos.y][pos.x - 1] != '#':
					openQ.append( [node, Coord(pos.x - 1, pos.y), steps + 1] )
			# Right
			if pos.x < (len(grid[pos.y]) - 1) and f"{pos.x + 1},{pos.y}" not in closed[node] and grid[pos.y][pos.x + 1] != '#':
					openQ.append( [node, Coord(pos.x + 1, pos.y), steps + 1] )

	return nodes

def graph_BFS(graph):
	'''search_start = time.process_time()
	setup_time = 0
	goal_check = 0
	closed_check = 0
	queue_add = 0'''

	# openQ format is a 2D list of [ Position, Inventory, Steps ]
	# closed is a dictionary of {Position: Inventory}
	closed = defaultdict(bool)
	openQ = deque()
	closed['@,'] = True
	openQ.append( State('@', list('.' * 26), '') )
	all_keys = list('.' * 26)

	# Determine goals and starting position
	for n in graph.keys():
		o = ord(n)
		if o >= 97:
			all_keys[o - 97] = n

	print(f"All Keys: {''.join(all_keys)}")

	# Search Loop
	while openQ:
		setup_start = time.process_time()
		current = openQ.popleft()
		name = current.name
		inv = list(current.inv)
		path = current.path

		print(f"  Open: {len(openQ)}, Closed: {len(closed)}      ", end="\r")				
		#setup_time += time.process_time() - setup_start

		# If you have every key in the level, you win!
		#goal_start = time.process_time()
		if inv == all_keys:
			#goal_check += time.process_time() - goal_start
			#search_time = time.process_time() - search_start
			'''print(f"Search Time: {search_time:.4f}")
			print(f"Setup Time: {setup_time:.4f} ({100*(setup_time/search_time):.2f}%)")
			print(f"Goal Check Time: {goal_check:.4f} ({100*(goal_check/search_time):.2f}%)")
			print(f"Checking if Closed Time: {closed_check:.4f} ({100*(closed_check/search_time):.2f}%)")
			print(f"Adding to Queue Time: {queue_add:.4f} ({100*(queue_add/search_time):.2f}%)")'''
			return current
		
		# Add all possible moves from this space to the openQ
		else:
			#goal_check += time.process_time() - goal_start
			for v in graph[name]:
				#closed_start = time.process_time()
				if f"{v.end},{inv}" not in closed and v.is_traversable(inv):
					#closed_check += time.process_time() - closed_start
					# Add this position and inventory to the closed list
					# If there's a new key in this spot, add it to the inventory as well
					queue_start = time.process_time()
					o = ord(v.end)
					if o >= 97 and inv[o - 97] == '.':
						hold_inv = list(inv)
						hold_inv[o - 97] = v.end
						closed[f"{v.end},{hold_inv}"] = True
						openQ.append( State(v.end, hold_inv, path + name) )
						#queue_add += time.process_time() - queue_start
					else:
						closed[f"{v.end},{inv}"] = True
						openQ.append( State(v.end, list(inv), path + name) )
						#queue_add += time.process_time() - queue_start

	#search_time = time.process_time() - search_start
	'''print(f"Search Time: {search_time:.4f}")
	print(f"Goal Check Time: {goal_check:.4f} ({100*(goal_check/search_time):.2f}%)")
	print(f"Checking if Closed Time: {closed_check:.4f} ({100*(closed_check/search_time):.2f}%)")
	print(f"Adding to Queue Time: {queue_add:.4f} ({100*(queue_add/search_time):.2f}%)")'''
	return None

def raw_BFS(grid):
	# openQ format is a 2D list of [ Position, Inventory, Steps ]
	# closed is a dictionary of {Position: Inventory}
	closed = defaultdict(bool)
	all_keys = list('.' * 26)

	# Determine goals and starting position
	for y in range( len(grid) ):
		for x in range( len(grid[y]) ):
			# Find the entrance and add it to openQ as the starting point
			if grid[y][x] == '@':
				openQ = [ [Coord(x, y), list('.' * 26), ''] ]
			# Find all keys in the grid and add them to the goal
			elif grid[y][x] in 'abcdefghijklmnopqrstuvwxyz':
				all_keys[ord(grid[y][x]) - 97] = grid[y][x]

	print(f"All Keys: {''.join(all_keys)}")

	# Search Loop
	while len(openQ) > 0:
		print(f"  Open: {len(openQ)}, Closed: {len(closed)}      ", end="\r")
		current = openQ.pop(0)
		pos = current[0]
		inv = current[1]
		path = current[2]

		#print(f"Position: {pos.x}, {pos.y} = {grid[pos.y][pos.x]}")
		#print(f"Keys: {inv}")
		#print(f"Steps: {steps}")

		# If there's a new key in this spot, add it to the inventory
		o = ord(grid[pos.y][pos.x])
		if o >= 97 and inv[o - 97] == '.':
				inv[o - 97] = grid[pos.y][pos.x]



		# If you have every key in the level, you win!
		if inv == all_keys:
			return pos, inv, path

		# Add all possible moves from this space to the openQ
		else:
			# Up
			if f"{pos.x},{pos.y - 1},{inv}" not in closed and is_traversable(grid[pos.y - 1][pos.x], inv):
				o = ord(grid[pos.y - 1][pos.x])
				if o >= 97 and inv[o - 97] == '.':
					hold_inv = list(inv)
					hold_inv[o - 97] = grid[pos.y - 1][pos.x]
					openQ.append( [Coord(pos.x, pos.y - 1), hold_inv, path + 'U'] )
					closed[f"{pos.x},{pos.y - 1},{hold_inv}"] = True
				else:
					openQ.append( [Coord(pos.x, pos.y - 1), inv, path + 'U'] )
					closed[f"{pos.x},{pos.y - 1},{inv}"] = True
			# Down
			if f"{pos.x},{pos.y + 1},{inv}" not in closed and is_traversable(grid[pos.y + 1][pos.x], inv):
				o = ord(grid[pos.y + 1][pos.x])
				if o >= 97 and inv[o - 97] == '.':
					hold_inv = list(inv)
					hold_inv[o - 97] = grid[pos.y + 1][pos.x]
					openQ.append( [Coord(pos.x, pos.y + 1), hold_inv, path + 'D'] )
					closed[f"{pos.x},{pos.y + 1},{hold_inv}"] = True
				else:
					openQ.append( [Coord(pos.x, pos.y + 1), inv, path + 'D'] )
					closed[f"{pos.x},{pos.y + 1},{inv}"] = True
			# Left
			if f"{pos.x - 1},{pos.y},{inv}" not in closed and is_traversable(grid[pos.y][pos.x - 1], inv):
				o = ord(grid[pos.y][pos.x - 1])
				if o >= 97 and inv[o - 97] == '.':
					hold_inv = list(inv)
					hold_inv[o - 97] = grid[pos.y][pos.x - 1]
					openQ.append( [Coord(pos.x - 1, pos.y), hold_inv, path + 'l'] )
					closed[f"{pos.x - 1},{pos.y},{hold_inv}"] = True
				else:
					openQ.append( [Coord(pos.x - 1, pos.y), inv, path + 'L'] )
					closed[f"{pos.x - 1},{pos.y},{inv}"] = True
			# Right
			if f"{pos.x + 1},{pos.y},{inv}" not in closed and is_traversable(grid[pos.y][pos.x + 1], inv):
				o = ord(grid[pos.y][pos.x + 1])
				if o >= 97 and inv[o - 97] == '.':
					hold_inv = list(inv)
					hold_inv[o - 97] = grid[pos.y][pos.x + 1]
					openQ.append( [Coord(pos.x + 1, pos.y), hold_inv, path + 'R'] )
					closed[f"{pos.x + 1},{pos.y},{hold_inv}"] = True
				else:
					openQ.append( [Coord(pos.x + 1, pos.y), inv, path + 'R'] )
					closed[f"{pos.x + 1},{pos.y},{inv}"] = True

	return None

def main():
	with open("inputs/day18.txt", "r") as file:
		grid = file.readlines()
		for y in range( len(grid) ):
			grid[y] = grid[y].strip()

		RAW_BFS = False

		if RAW_BFS:
			pos, inv, path = raw_BFS(grid)
			print(f"Final Position: ({pos.x}, {pos.y}), Inventory: {''.join(inv)}, Path Length: {len(path)}")
		else:
			graph = generate_graph(grid)
			print()
			for node in graph.keys():
				print(f"{node}: ", end='')
				for v in graph[node]:
					print(f"({v.end}, {v.length}, {v.key}), ", end='')
				print()

			node = graph_BFS(graph)
			print()
			print(f"Final Node: {node}")

			# Calculate path length
			path = node.path
			path += node.name
			steps = 0
			prev_node = path[0]
			for n in path[1:]:
				for v in graph[prev_node]:
					if v.end == n:
						steps += v.length
						break
				prev_node = n

			print(f"Steps: {steps}")

if __name__ == "__main__":
	main()
