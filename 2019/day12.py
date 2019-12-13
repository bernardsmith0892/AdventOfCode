#!/usr/bin/local/python3.7

class Moon:
	x,y,z = 0,0,0
	i,j,k = 0,0,0

	def __init__(self, x=0, y=0, z=0, i=0, j=0, k=0):
		self.x = x
		self.y = y
		self.z = z
		
		self.i = i
		self.j = j
		self.k = k

	def gravity_pull(self, other_moon):
		if other_moon.x < self.x:
			self.i -= 1
		elif other_moon.x > self.x:
			self.i += 1

		if other_moon.y < self.y:
			self.j -= 1
		elif other_moon.y > self.y:
			self.j += 1

		if other_moon.z < self.z:
			self.k -= 1
		elif other_moon.z > self.z:
			self.k += 1

	def move(self):
		self.x += self.i
		self.y += self.j
		self.z += self.k

	def potential_energy(self):
		return abs(self.x) + abs(self.y) + abs(self.z)

	def kinetic_energy(self):
		return abs(self.i) + abs(self.j) + abs(self.k)

	def total_energy(self):
		return self.potential_energy() * self.kinetic_energy()

	def to_string(self):
		return f"{self.x},{self.y},{self.z},{self.i},{self.j},{self.k}"

def moon_list_to_string(moon):
	ret_str = ''
	for m in moon:
		ret_str += m.to_string() + ','

	return ret_str[:-1]

def moon_x_to_string(moon):
	ret_str = ''
	for m in moon:
		ret_str += f"{m.x},{m.i},"

	return ret_str[:-1]	

def moon_y_to_string(moon):
	ret_str = ''
	for m in moon:
		ret_str += f"{m.y},{m.j},"

	return ret_str[:-1]	

def moon_z_to_string(moon):
	ret_str = ''
	for m in moon:
		ret_str += f"{m.z},{m.k},"

	return ret_str[:-1]	

def find_period(moon, axis):
	history = {}
	steps = 0

	if axis == 'x':
		status_string = moon_x_to_string(moon)
	elif axis == 'y':
		status_string = moon_y_to_string(moon)
	else:
		status_string = moon_z_to_string(moon)

	while status_string not in history:
		history[status_string] = True

		moon[0].gravity_pull(moon[1])
		moon[0].gravity_pull(moon[2])
		moon[0].gravity_pull(moon[3])

		moon[1].gravity_pull(moon[0])
		moon[1].gravity_pull(moon[2])
		moon[1].gravity_pull(moon[3])

		moon[2].gravity_pull(moon[0])
		moon[2].gravity_pull(moon[1])
		moon[2].gravity_pull(moon[3])

		moon[3].gravity_pull(moon[0])
		moon[3].gravity_pull(moon[1])
		moon[3].gravity_pull(moon[2])

		for m in moon:
			m.move()

		if axis == 'x':
			status_string = moon_x_to_string(moon)
		elif axis == 'y':
			status_string = moon_y_to_string(moon)
		else:
			status_string = moon_z_to_string(moon)

		steps += 1
		#print(f' Steps: {steps}', end='\r')

	#print(f' Steps: {steps}')
	return steps

def LCM(a, b):
	if(a > b):
		num = a
		den = b
	else:
		num = b
		den = a
	rem = num % den

	while rem != 0:
		num = den
		den = rem
		rem = num % den

	gcd = den
	lcm = (a * b) // gcd

	return lcm

def LCM_list(num_array):
	ans = num_array[0]
	lcm = 0

	for n in num_array[1:]:
		lcm = LCM(ans, n)
		ans = lcm

	return lcm


def part1():
	'''
	<x=14, y=2, z=8>
	<x=7, y=4, z=10>
	<x=1, y=17, z=16>
	<x=-4, y=-1, z=1>
	'''

	moon = []
	
	moon.append(Moon(14, 2, 8))
	moon.append(Moon(7, 4, 10))
	moon.append(Moon(1, 17, 16))
	moon.append(Moon(-4, -1, 1))
	

	'''
	moon.append(Moon(-8, -10, 0))
	moon.append(Moon(5, 5, 10))
	moon.append(Moon(2, -7, 3))
	moon.append(Moon(9, -8, -3))
	'''
	for x in range(1000):
		moon[0].gravity_pull(moon[1])
		moon[0].gravity_pull(moon[2])
		moon[0].gravity_pull(moon[3])

		moon[1].gravity_pull(moon[0])
		moon[1].gravity_pull(moon[2])
		moon[1].gravity_pull(moon[3])

		moon[2].gravity_pull(moon[0])
		moon[2].gravity_pull(moon[1])
		moon[2].gravity_pull(moon[3])

		moon[3].gravity_pull(moon[0])
		moon[3].gravity_pull(moon[1])
		moon[3].gravity_pull(moon[2])

		for m in moon:
			m.move()

	total_energy = 0
	for m in moon:
		total_energy += m.total_energy()

	print(total_energy)	

def part2():
	moon = []
	history = {}
	steps = 0
	
	
	moon.append(Moon(14, 2, 8))
	moon.append(Moon(7, 4, 10))
	moon.append(Moon(1, 17, 16))
	moon.append(Moon(-4, -1, 1))
	

	'''
	moon.append(Moon(-1, 0, 2))
	moon.append(Moon(2, -10, -7))
	moon.append(Moon(4, -8, 8))
	moon.append(Moon(3, 5, -1))
	'''

	x_period = find_period(moon, 'x')
	print(f"X Period: {x_period}")

	y_period = find_period(moon, 'y')
	print(f"Y Period: {y_period}")

	z_period = find_period(moon, 'z')
	print(f"Z Period: {z_period}")

	print(f"Period of System: {LCM_list([x_period,y_period,z_period])}")

	'''
	status_string = moon_list_to_string(moon)
	while status_string not in history:
		history[status_string] = True

		moon[0].gravity_pull(moon[1])
		moon[0].gravity_pull(moon[2])
		moon[0].gravity_pull(moon[3])

		moon[1].gravity_pull(moon[0])
		moon[1].gravity_pull(moon[2])
		moon[1].gravity_pull(moon[3])

		moon[2].gravity_pull(moon[0])
		moon[2].gravity_pull(moon[1])
		moon[2].gravity_pull(moon[3])

		moon[3].gravity_pull(moon[0])
		moon[3].gravity_pull(moon[1])
		moon[3].gravity_pull(moon[2])

		for m in moon:
			m.move()

		status_string = moon_list_to_string(moon)
		steps += 1
		print(f' Steps: {steps}', end='\r')
	'''





part1()
part2()