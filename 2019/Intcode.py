#!/usr/local/bin/python3.7

import sys

DEBUG = False
DEBUG_RANGE = 6


''' Adds a and b. Stores the result in target. '''
def add(a, b, target, mode, memory):
	# Mode Control
	a = memory[a] if mode[0] == 0 else a
	b = memory[b] if mode[1] == 0 else b

	# Actions
	memory[target] = a + b

	if DEBUG:
		print(f"{a} + {b} = {memory[target]}. Stored in {target}.")

	return 4

''' Multiplies a and b. Stores the result in target. '''
def multiply(a, b, target, mode, memory):
	# Mode Control
	a = memory[a] if mode[0] == 0 else a
	b = memory[b] if mode[1] == 0 else b

	# Actions
	memory[target] = a * b

	if DEBUG:
		print(f"{a} * {b} = {memory[target]}. Stored in {target}.")

	return 4

''' Accepts interactive user input and stores it in target. '''
def input_memory(target, mode, memory):
	memory[target] = int(input(f"Input: "))

	if DEBUG:
		print(f"Stored {memory[target]} in {target}.")

	return 2

''' Accepts automated input from input_data param and stores it in target. '''
def input_memory_automated(input_data, target, mode, memory):
	memory[target] = input_data

	if DEBUG:
		print(f"Stored {memory[target]} in {target}.")

	return 2

''' Outputs value of target to STDOUT. '''
def output_memory(target, mode, memory):
	# Mode Control
	target = memory[target] if mode[0] == 0 else target

	# Actions
	print(f"{target}")

	return 2

''' Returns the value of the target for use by other scripts. '''
def output_memory_automated(target, mode, memory):
	# Mode Control
	target = memory[target] if mode[0] == 0 else target

	# Actions
	return target

''' Tests if target value != 0. Returns address to jump to, if true. Returns a None type if false. Receiving a None type implies moving the position value normally. (by 3) '''
def jump_true(test, target, mode, memory):
	# Mode Control
	test = memory[test] if mode[0] == 0 else test
	target = memory[target] if mode[1] == 0 else target

	if DEBUG:
		print(f"Testing if {test} != 0. Jumping to {target}, if true.")

	# Actions
	return target if test != 0 else None

''' Tests if target value == 0. Returns address to jump to, if true. Returns a None type if false. Receiving a None type implies moving the position value normally. (by 3) '''
def jump_false(test, target, mode, memory):
	# Mode Control
	test = memory[test] if mode[0] == 0 else test
	target = memory[target] if mode[1] == 0 else target

	if DEBUG:
		print(f"Testing if {test} == 0. Jumping to {target}, if true.")

	# Actions
	return target if test == 0 else None

''' Tests a < b. Store 1 in target if true. 0 if false. '''
def less_than(a, b, target, mode, memory):
	# Mode Control
	a = memory[a] if mode[0] == 0 else a
	b = memory[b] if mode[1] == 0 else b

	# Actions
	memory[target] = 1 if a < b else 0

	if DEBUG:
		print(f"{a} < {b} = {memory[target]}. Stored in {target}.")

	return 4

''' Tests a == b. Store 1 in target if true. 0 if false. '''
def equals(a, b, target, mode, memory):
	# Mode Control
	a = memory[a] if mode[0] == 0 else a
	b = memory[b] if mode[1] == 0 else b

	# Actions
	memory[target] = 1 if a == b else 0

	if DEBUG:
		print(f"{a} == {b} = {memory[target]}. Stored in {target}.")

	return 4

''' Decodes the mode settings for an instruction value. Returns the opcode and list of modes in a tuple '''
def decode_instruction(instruction):
	mode = [0, 0, 0]

	opcode = instruction % 100
	mode[0] = (instruction // 100) % 10
	mode[1] = (instruction // 1000) % 10
	mode[2] = (instruction // 10000) % 10

	if DEBUG:
		print(f"Decoding {instruction} into => Opcode: {opcode}, Modes: {mode}")

	return opcode, mode

''' Reads and executes an Intcode program. '''
def run_program(filename):
	# Open Intcode file
	with open(filename, "r") as memory:
		memory = list(map(int, memory.readline().split(',')))

		# Main Loop
		position = 0
		step = 1
		skip_until = 0
		while position < len(memory):
			if DEBUG:
				print(f"Position: {position}, Step: {step}")

				start = position# - DEBUG_RANGE
				stop = position + DEBUG_RANGE
				start = 0 if start < 0 else start
				stop = len(memory) - 1 if stop > len(memory) - 1 else stop

				print(memory[ start : stop ])
			# Decodes the instruction at the current memory position
			opcode, mode = decode_instruction( memory[position] )

			if opcode == 1: # Add
				position += add(memory[position + 1], memory[position + 2], memory[position + 3], mode, memory)
			
			elif opcode == 2: # Multiply
				position += multiply(memory[position + 1], memory[position + 2], memory[position + 3], mode, memory)
			
			elif opcode == 3: # User Input
				position += input_memory(memory[position + 1], mode, memory)
			
			elif opcode == 4: # Output Value
				position += output_memory(memory[position + 1], mode, memory)
			
			elif opcode == 5: # Jump If True
				result = jump_true(memory[position + 1], memory[position + 2], mode, memory)
				position = result if result != None else position + 3
			
			elif opcode == 6: # Jump If False
				result = jump_false(memory[position + 1], memory[position + 2], mode, memory)
				position = result if result != None else position + 3
			
			elif opcode == 7: # Less Than
				position += less_than(memory[position + 1], memory[position + 2], memory[position + 3], mode, memory)
			
			elif opcode == 8: # Equals
				position += equals(memory[position + 1], memory[position + 2], memory[position + 3], mode, memory)
			
			elif opcode == 99: # Halt Program
				return
			
			else: # Error if the current memory position does not decode into a valid instruction.
				print(f"ERROR! Unknown opcode {opcode} from {memory[position]} at position {position}.")
				print(memory)
				break

			if DEBUG:
				if step > skip_until:
					skip_input = input("...")
					skip_until = 0 if skip_input == "" else int(skip_input) + step
				else:
					print("...")

			step += 1

''' A self-contained execution of an Intcode program '''
class VM:
	memory = []
	input_queue = []
	output_queue = []
	position = 0

	def __init__(self, filename):
		with open(filename, "r") as file:
			self.memory = list(map(int, file.readline().split(',')))
		self.position = 0
		self.input_queue = []
		self.output_queue = []

	''' Execute one instruction in the VM's program. Returns True if running normally. Returns False if halted. (Opcode 99) Returns None if awaiting input. '''
	def step(self):
		opcode, mode = decode_instruction( self.memory[ self.position ] )

		if opcode == 1: # Add
			self.position += add(self.memory[self.position + 1], self.memory[self.position + 2], self.memory[self.position + 3], mode, self.memory)
		
		elif opcode == 2: # Multiply
			self.position += multiply(self.memory[self.position + 1], self.memory[self.position + 2], self.memory[self.position + 3], mode, self.memory)
		
		elif opcode == 3: # Pass input from the input queue into the program
			if len(self.input_queue) != 0:
				self.position += input_memory_automated(self.input_queue.pop(0), self.memory[self.position + 1], mode, self.memory)
			else:
				return None
		
		elif opcode == 4: # Adds output from the program into the output queue
			result = output_memory_automated(self.memory[self.position + 1], mode, self.memory)
			self.output_queue.append(result)

			self.position += 2
		
		elif opcode == 5: # Jump If True
			result = jump_true(self.memory[self.position + 1], self.memory[self.position + 2], mode, self.memory)
			self.position = result if result != None else self.position + 3
		
		elif opcode == 6: # Jump If False
			result = jump_false(self.memory[self.position + 1], self.memory[self.position + 2], mode, self.memory)
			self.position = result if result != None else self.position + 3
		
		elif opcode == 7: # Less Than
			self.position += less_than(self.memory[self.position + 1], self.memory[self.position + 2], self.memory[self.position + 3], mode, self.memory)
		
		elif opcode == 8: # Equals
			self.position += equals(self.memory[self.position + 1], self.memory[self.position + 2], self.memory[self.position + 3], mode, self.memory)
		
		elif opcode == 99: # Halt Program
			return False
		
		else: # Error if the current self.memory self.position does not decode into a valid instruction.
			print(f"ERROR! Unknown opcode {opcode} from {self.memory[self.position]} at self.position {self.position}.")
			print(self.memory)
			return "ERROR"

		return True

	def add_to_input_queue(self, new_input):
		self.input_queue.append(new_input)

	def read_from_output_queue(self):
		return self.output_queue.pop(0)

	def output_in_queue(self):
		return len(self.output_queue) > 0

	def print_status(self):
		print(f"Position: {self.position}")

		start = self.position
		stop = self.position + 5
		start = 0 if start < 0 else start
		stop = len(self.memory) - 1 if stop > len(self.memory) - 1 else stop

		print(self.memory[ start : stop ])

		print(f"Input Queue: {self.input_queue}")
		print(f"Output Queue: {self.output_queue}")


def main():
	try:
		if sys.argv[2] == "DEBUG":
			global DEBUG
			DEBUG = True
	except:
		pass

	run_program(sys.argv[1])

if __name__ == '__main__':
	main()




















