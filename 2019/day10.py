import math

def angle_between(a, b):
#	dot = a[0]*b[0] + a[1]*b[1]
#	det = a[0]*b[1] - a[1]*b[0]
	x = a[0] - b[0]
	y = a[1] - b[1]

	theta = math.degrees(math.atan2(x, y));

	if theta < 0.0:
		theta += 360.0

	return 360.0 - theta if theta != 0 else theta

def asteroids_in_view(location, asteroids):
	angles = {}
	for a in asteroids:
		if a[0] != location[0] or a[1] != location[1]:
			current_angle = angle_between(location, a)
			if current_angle not in angles:
				angles[current_angle] = [a]
			else:
				angles[current_angle].append(a)

	return angles

def closest_asteroid(location, asteroids):
	dist = [-1, (0,0)]

	for a in asteroids:
		current_dist = math.sqrt(((a[0] - location[0]) ** 2) + ((a[1] - location[1]) ** 2))
		if current_dist < dist[0] or dist[0] == -1:
			dist = [current_dist, a]

	return dist[1]

def vaporization_list(location, asteroids):
	vaporization_order = []
	angles = asteroids_in_view(location, asteroids)
	angles_list = list(angles.keys())
	angles_list.sort()
	#print(angles)
	#print(angles_list)

	while len(vaporization_order) < len(asteroids) - 1:
		for a in angles_list:
			if len(angles[a]) > 0:
				closest = closest_asteroid(location, angles[a])
				angles[a].remove(closest)
				vaporization_order.append(closest)

	return vaporization_order





asteroids = []

with open("inputs/day10.txt", "r") as data:
	data = data.readlines()

	x,y = 0,0
	for line in data:
		for c in line:
			if c == "#":
				asteroids.append( (x,y) ) 
			x += 1
		x = 0
		y += 1

# print(f"List of Asteroids: {asteroids}")

max_los = [0, (0,0)]

for a in asteroids:
	current_los = len( asteroids_in_view(a, asteroids).keys() )
	# print(f"{current_los}, {a}")
	if current_los > max_los[0]:
		max_los = [current_los, a]

print(f"Best Location: {max_los}")
#print(asteroids_in_view(max_los[1], asteroids))

print(vaporization_list(max_los[1], asteroids)[199])