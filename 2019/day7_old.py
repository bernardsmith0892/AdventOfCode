#!/usr/local/bin/python3.7

import pexpect
import itertools 

def run_amplifier(phase, input_value):
	child = pexpect.spawn('python3.7 Intcode.py inputs/day7.txt')
	child.expect("Input: ")
	child.sendline(str(phase)) # Phase
	child.expect("Input: ")
	child.sendline(str(input_value)) # Input
	return int(child.readlines()[1].strip().decode('utf-8'))

def run_circuit(phase_settings, input_value = 0):
	for phase in phase_settings:
		input_value = run_amplifier(phase, input_value)

	return input_value

def run_feedback_circuit(phase_settings, input_value = 0):
	# NOT WORKING
	amp = []
	output = input_value
	for c in range(5):
		amp.append(pexpect.spawn('python3.7 Intcode.py inputs/day7_test.txt'))

	while not amp[4].eof():
		for a in range(len(amp)):
			try:
				amp[a].expect("Input: ")
				amp[a].sendline(str(phase_settings[a])) # Phase
				amp[a].expect("Input: ")
				amp[a].sendline(str(output)) # Input
				print(f"Amp {a}: {amp[a].readline().strip().decode('utf-8')}", end=", Output = ")
				output = int(amp[a].readline().strip().decode('utf-8'))
				print(output)			
			except Exception as e:
				pass

	iteration = 0
	amp = []
	for c in range(5):
		amp.append(pexpect.spawn('python3.7 Intcode.py inputs/day7_test.txt'))

	while iteration < 2:
		for a in range(len(amp)):
			try:
				amp[a].expect("Input: ")
				amp[a].sendline(str(phase_settings[a])) # Phase
				amp[a].expect("Input: ")
				amp[a].sendline(str(output)) # Input
				print(f"Amp {a}: {amp[a].readline().strip().decode('utf-8')}", end=", Output = ")
				output = int(amp[a].readline().strip().decode('utf-8'))
				print(output)			
			except Exception as e:
				pass

		iteration += 1

	return output

def part1():
	possible_settings = list(itertools.permutations([0,1,2,3,4]))
	max_output = (0, [])

	for phase_setting in possible_settings:
		output = run_circuit(phase_setting)

		if output > max_output[0]:
			max_output = (output, phase_setting)

	print(max_output)

def part2():
	# NOT WORKING
	possible_settings = list(itertools.permutations([5,6,7,8,9]))
	max_output = (0, [])

	combination = 1
	max_combinations = 120
	for phase_setting in possible_settings:
		output = run_feedback_circuit(phase_setting)

		if output > max_output[0]:
			print(f"NEW MAX: {output}, From Settings: {phase_setting} ({combination} of {max_combinations})")
			max_output = (output, phase_setting)
		else:
			print(f"Lesser Output: {output}, From Settings: {phase_setting} ({combination} of {max_combinations})")

		combination += 1

	print(f"MAXIMUM OUTPUT = {max_output}")

# part2()
print(run_feedback_circuit([9,7,8,5,6], 0))


