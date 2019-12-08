#!/usr/local/bin/python3.7

import Intcode
import itertools

def run_circuit(phase_settings, input_value = 0):
	amps = []
	results = [1,1,1,1,1]
	focus = 0
	for a in range(5):
		amps.append( Intcode.VM('inputs/day7.txt') )	

	for i in range( len(phase_settings) ):
		amps[i].add_to_input_queue(phase_settings[i])

	amps[0].add_to_input_queue(input_value)

	while results[4] != False:
		results[focus] = amps[focus].step()

		if amps[focus].output_in_queue():
			amps[(focus + 1) % 5].add_to_input_queue( amps[focus].read_from_output_queue() )

		focus = (focus + 1)  % 5

	return amps[0].input_queue[0]

def part1():
	possible_settings = list(itertools.permutations([0,1,2,3,4]))
	max_output = (0, [])

	for phase_setting in possible_settings:
		output = run_circuit(phase_setting)
		
		if output > max_output[0]:
			max_output = output,phase_setting

	print(f"Highest Signal: {max_output[0]}, Phase Settings: {max_output[1]}")


def part2():
	possible_settings = list(itertools.permutations([5,6,7,8,9]))
	max_output = (0, [])

	for phase_setting in possible_settings:
		output = run_circuit(phase_setting)
		
		if output > max_output[0]:
			max_output = output,phase_setting

	print(f"Highest Signal: {max_output[0]}, Phase Settings: {max_output[1]}")


def main():
	print("Part 1:")
	part1()
	print("Part 2:")
	part2()

if __name__ == '__main__':
	main()




















