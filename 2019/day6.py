#!/usr/local/bin/python3.7

def count_orbits(obj, orbit_list, discovered, orbits = 0):
	if orbit_list[obj] == "COM":
		return orbits + 1
	else:
		return count_orbits(orbit_list[obj], orbit_list, orbits + 1)

def find_orbit_path(orbit_list, start = "YOU", end = "SAN"):
	start = [start]
	queue = [start]
	discovered = [start]	

	while len(queue) > 0:
		print(f"Queue Size: {len(queue)}, Discovered Nodes: {len(discovered)}", end="\r")
		v = queue.pop(0)
		if v[0] == end:
			print()	
			return v
		else:
			for w in orbit_list[v[0]]:
				if w not in discovered:
					discovered.append(w)
					w = [w] + v
					queue.append(w)

orbit_list = {}
with open("inputs/day6.txt", "r") as file:
	for line in file.readlines():
		line = line.strip().split(")")

		if line[1] not in orbit_list:
			orbit_list[ line[1] ] = [ line[0] ]
		else:
			orbit_list[ line[1] ].append(line[0])

		if line[0] not in orbit_list:
			orbit_list[ line[0] ] = [ line[1] ]
		else:
			orbit_list[ line[0] ].append(line[1])

	#orbits = 0
	#for obj in orbit_list.keys():
	#	orbits += count_orbits(obj, orbit_list)
	path = find_orbit_path(orbit_list);

	print(path)
	print(len(path[1:-1]) - 1)


