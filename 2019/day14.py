#!/usr/local/bin/python3.7

''' Interpretation of a chemical formula '''
class Reaction:
	result = ''
	requirements = {}

	''' Converts an ASCII formula to its object interpretation '''
	def __init__(self, formula):
		self.requirements = {}

		result = formula.split('>')[1]
		requirements = formula.split('=')[0].split(',')

		self.result = ( result.strip().split(' ')[1], int(result.strip().split(' ')[0]) )

		for r in requirements:
			self.requirements[ r.strip().split(' ')[1] ] = int(r.strip().split(' ')[0])

	def print_formula(self):
		for r in self.requirements.keys():
			print(f"{self.requirements[r]} {r} ", end='')

		print(f"=> {self.result[1]} {self.result[0]}")

	''' Checks if the given chemical can be produced by this reaction '''
	def is_produced_by(self, chemical):
		if chemical[0] == self.result[0]:
			return self.result[1] <= chemical[1]
		else:
			return False

	''' Adjusts the given inventory based on performing this reaction in reverse.
	    An imperfect reaction allows for negative results, which implies excess resources. '''
	def reverse_reaction(self, inventory, imperfect=False):
		# Determine the amount of times this reaction can be performed, given a perfect reaction.
		if not imperfect:
			ratio = inventory[ self.result[0] ] // self.result[1]
		else:
			ratio = 1

		# Adjust the inventory based on the reaction's requirements and result
		inventory[ self.result[0] ] -= self.result[1] * ratio
		for r in self.requirements.keys():
			if r in inventory:
				inventory[r] += self.requirements[r] * ratio
			else:
				inventory[r] = self.requirements[r] * ratio


def to_string(chemicals):
	return_str = ""

	for k in chemicals.keys():
		return_str += str(chemicals[k]) + ' ' + k + ', '

	return return_str[:-2]

''' Remove all chemicals in the inventory with zero amounts '''
def remove_zeros(inventory):
	to_delete = []
	for i in inventory.keys():
		if inventory[i] == 0:
			to_delete.append(i)

	for d in to_delete:
		del inventory[d]

''' Part 1: Finds the minimum ore needed to created the given fuel.
	Searches backwards from the final result (e.g. 1 FUEL) and determines 
	the required resources to create it. '''
def minimum_ore(reactions, fuel=1):
	inventory = {'FUEL': fuel}
	
	# Assume all reactions result in no excess materials
	perfect_reactions = True
	while perfect_reactions:
		perfect_reactions = False
		for r in reactions:
			for i in inventory.keys():
				if r.is_produced_by( (i, inventory[i]) ):
					perfect_reactions = True
					r.reverse_reaction(inventory)
					break

	# Allow reactions that create excess materials
	imperfect_reactions = True
	while imperfect_reactions:
		imperfect_reactions = False
		for r in reactions:
			for i in inventory.keys():
				if r.result[0] == i and inventory[i] > 0:
					imperfect_reactions = True
					r.reverse_reaction(inventory, imperfect=True)
					break

	remove_zeros(inventory)
	return inventory['ORE']

''' Perform a psuedo-binary search for the border between 1 trillion ore '''
def maximum_fuel(reactions, min_ore=1, input_ore=1000000000000):
	# Set the initial lower bound be a naive calculation of required ore divided by the ore needed to create 1 FUEL
	fuel = input_ore // min_ore
	prior_fuel = fuel
	ore = fuel * min_ore

	# Search from the lower bound exponentially until the result is greater than input_ore
	increase = 1
	while ore < input_ore:
		prior_fuel = fuel
		fuel += increase
		increase = increase * 2
		ore = minimum_ore(reactions, fuel)
		#print(f" {ore}: {100 * (ore / input_ore):.4f}%", end='\r')

	# Perform a binary-search bracketed between the latest result and the result previously tested
	#print()
	max_fuel = fuel
	min_fuel = prior_fuel
	fuel = (max_fuel + min_fuel) // 2
	ore = minimum_ore(reactions, min_fuel)
	while True:
		ore = minimum_ore(reactions, fuel)
		#print(f" {ore}: {100 * (ore / input_ore):.4f}%", end='\r')

		if ore > input_ore and fuel < max_fuel:
			max_fuel = fuel
		elif ore < input_ore and fuel > min_fuel:
			min_fuel = fuel
		elif ore == input_ore:
			break
		elif max_fuel == min_fuel:
			break
		elif max_fuel == (min_fuel + 1):
			break

		fuel = (max_fuel + min_fuel) // 2

	#print()
	ore = minimum_ore(reactions, fuel - 1)
	#print(f" {ore}: {100 * (ore / input_ore):.4f}%")

	return fuel
	

def main():
	reactions = []
	with open("inputs/day14.txt") as data:
		for line in data.readlines():
			new_reaction = Reaction(line)
			reactions.append( new_reaction )

	#for r in reactions:
	#	r.print_formula()

	ore = minimum_ore(reactions, 1)
	print(f"Part 1: {ore} ORE")

	print(f"Part 2: {maximum_fuel(reactions, ore)} FUEL")


if __name__ == '__main__':
	main()
