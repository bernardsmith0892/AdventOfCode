#!/usr/local/bin/python3.7

import sys

DEBUG = False
DEBUG_RANGE = 6


''' A self-contained execution of an Intcode program '''
class VM:
	memory = []
	input_queue = []
	output_queue = []
	position = 0
	relative_base = 0
	automated = False

	def __init__(self, filename, automated = False):
		with open(filename, "r") as file:
			self.memory = list(map(int, file.readline().split(',')))

		# self.pad_memory(size)

		self.position = 0
		self.relative_base = 0
		self.input_queue = []
		self.output_queue = []
		self.automated = automated

	def run(self):
		status = True
		while status:
			if DEBUG:
				self.print_status()

			status = self.step()

			if DEBUG:
				input("...")


	''' Execute one instruction in the VM's program. Returns True if running normally. Returns False if halted. (Opcode 99) Returns None if awaiting input. '''
	def step(self):
		opcode, params = self.decode_instruction( self.memory[ self.position ] )

		if opcode == 1: # Add
			self.add(params)
		
		elif opcode == 2: # Multiply
			self.multiply(params)
		
		elif opcode == 3: # Pass input from the input queue into the program
			if self.automated:
				if len(self.input_queue) != 0:
					self.input_memory_automated(self.input_queue.pop(0), params)
				else:
					return None
			else:
				self.input_memory(params)
		
		elif opcode == 4: # Adds output from the program into the output queue
			if self.automated:
				self.output_queue.append( self.output_memory_automated(params) )
			else:
				self.output_memory(params)
		
		elif opcode == 5: # Jump If True
			result = self.jump_true(params)
		
		elif opcode == 6: # Jump If False
			result = self.jump_false(params)
		
		elif opcode == 7: # Less Than
			self.less_than(params)
		
		elif opcode == 8: # Equals
			self.equals(params)

		elif opcode == 9: # Change Relative Base
			self.adjust_relative_base(params)
		
		elif opcode == 99: # Halt Program
			return False
		
		else: # Error if the current self.memory self.position does not decode into a valid instruction.
			print(f"ERROR! Unknown opcode {opcode} from {self.memory[self.position]} at self.position {self.position}.")
			print(self.memory)
			return False

		return True

	def add_to_input_queue(self, new_input):
		self.input_queue.append(int(new_input))

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

		# print(self.memory[ start : stop ])
		print(self.memory)

		print(f"Input Queue: {self.input_queue}")
		print(f"Output Queue: {self.output_queue}")

	''' Adds a and b. Stores the result in target. '''
	def add(self, params):
		a = params[0]
		b = params[1]
		target = params[2]

		self.memory[target] = a + b

		if DEBUG:
			print(f"{a} + {b} = {self.memory[target]}. Stored in {target}.")

		self.position += 4

	''' Multiplies a and b. Stores the result in target. '''
	def multiply(self, params):
		a = params[0]
		b = params[1]
		target = params[2]
		
		self.memory[target] = a * b

		if DEBUG:
			print(f"{a} * {b} = {self.memory[target]}. Stored in {target}.")

		self.position += 4

	''' Accepts interactive user input and stores it in target. '''
	def input_memory(self, params):
		target = params[0]

		self.memory[target] = int(input(f"Input: "))

		if DEBUG:
			print(f"Stored {self.memory[target]} in {target}.")

		self.position += 2

	''' Accepts automated input from input_data param and stores it in target. '''
	def input_memory_automated(self, input_data, params):
		target = params[0]

		self.memory[target] = input_data

		if DEBUG:
			print(f"Stored {self.memory[target]} in {target}.")

		self.position += 2

	''' Outputs value of target to STDOUT. '''
	def output_memory(self, params):
		target = params[0]

		print(f"{target}")

		self.position += 2

	''' Returns the value of the target for use by other scripts. '''
	def output_memory_automated(self, params):
		target = params[0]

		self.position += 2
		
		# Actions
		return target

	''' Tests if target value != 0. Returns address to jump to, if true. Returns a None type if false. Receiving a None type implies moving the position value normally. (by 3) '''
	def jump_true(self, params):
		test = params[0]
		target = params[1]

		if DEBUG:
			print(f"Testing if {test} != 0. Jumping to {target}, if true.")

		# Actions
		self.position = target if test != 0 else self.position + 3

	''' Tests if target value == 0. Returns address to jump to, if true. Returns a None type if false. Receiving a None type implies moving the position value normally. (by 3) '''
	def jump_false(self, params):
		test = params[0]
		target = params[1]

		if DEBUG:
			print(f"Testing if {test} == 0. Jumping to {target}, if true.")

		# Actions
		self.position = target if test == 0 else self.position + 3

	''' Tests a < b. Store 1 in target if true. 0 if false. '''
	def less_than(self, params):
		a = params[0]
		b = params[1]
		target = params[2]

		self.memory[target] = 1 if a < b else 0

		if DEBUG:
			print(f"{a} < {b} = {self.memory[target]}. Stored in {target}.")

		self.position += 4

	''' Tests a == b. Store 1 in target if true. 0 if false. '''
	def equals(self, params):
		a = params[0]
		b = params[1]
		target = params[2]

		# Actions
		self.memory[target] = 1 if a == b else 0

		if DEBUG:
			print(f"{a} == {b} = {self.memory[target]}. Stored in {target}.")

		self.position += 4

	def adjust_relative_base(self, params):
		change = params[0]

		self.relative_base += change

		if DEBUG:
			print(f"Changing relative base to {self.relative_base}.")

		self.position += 2

	''' Decodes the mode settings for an instruction value. Returns the opcode and list of params in a tuple '''
	def decode_instruction(self, instruction, disassembling=False):
		mode = []
		params = []

		# A dictonary of what parameters are used to store to memory for each opcode.
		storage_params = {
		1 : '001',
		2 : '001',
		3 : '1',
		4 : '0',
		5 : '00',
		6 : '00',
		7 : '001',
		8 : '001',
		9 : '0',
		99 : ''
		}

		# Extract the opcode
		opcode = instruction % 100

		# Halt if we're disassembling and this is an invalid opcode. Allows us to print this opcode as memory space.
		# Will eventually throw an exception if we're not disassembling
		if opcode not in storage_params and disassembling:
			return opcode, mode

		# Extract the parameter modes
		for m in range( len(storage_params[opcode]) ):
			mode.append( (instruction // (10 ** (m + 2)) ) % 10 )

		# Only return the opcode and mode if we're disassembling the Intcode
		if disassembling:
			return opcode, mode

		# Retrieve the parameters from memory based on the modes
		for m in range( len(mode) ):
			# Cases for when the given parameter is NOT an address to store to memory
			if storage_params[opcode][m] == '0':
				if mode[m] == 0:
					# Add more memory space if this will attempt to access uninitialized memory
					if self.memory[ self.position + m + 1 ] >= len(self.memory):
						self.pad_memory( self.memory[ self.position + m + 1 ] + 1 )
					params.append( self.memory[ self.memory[ self.position + m + 1 ] ] )
				elif mode[m] == 1:
					params.append( self.memory[ self.position + m + 1 ] )
				elif mode[m] == 2:
					# Add more memory space if this will attempt to access uninitialized memory
					if self.relative_base + self.memory[ self.position + m + 1 ] >= len(self.memory):
						self.pad_memory( self.relative_base + self.memory[ self.position + m + 1 ] + 1 )
					params.append( self.memory[ self.relative_base + self.memory[ self.position + m + 1 ] ] )
			
			# Cases for when the instruction is supposed to use this paramter to store to memory
			else:
				if mode[m] == 2:
					# Add more memory space if this will attempt to access uninitialized memory
					if self.memory[ self.position + m + 1 ] + self.relative_base >= len(self.memory):
						self.pad_memory( self.memory[ self.position + m + 1 ] + self.relative_base + 1 )	
					params.append( self.memory[ self.position + m + 1 ] + self.relative_base )
				else:
					# Add more memory space if this will attempt to access uninitialized memory
					if self.memory[ self.position + m + 1 ] >= len(self.memory):
						self.pad_memory( self.memory[ self.position + m + 1 ] + 1 )
					params.append( self.memory[ self.position + m + 1 ] )

		if DEBUG:
			print(f"Decoding {instruction} into => Opcode: {opcode}, Modes: {mode}, Params: {params}")

		return opcode, params

	'''
	Print out the current memory space using mnemonic keywords
	'''
	def disassemble(self):
		mnemonics = {
		1 : 'add',
		2 : 'mul',
		3 : 'input',
		4 : 'output',
		5 : 'jnz',
		6 : 'jz',
		7 : 'less',
		8 : 'eq',
		9 : 'mvrb',
		99 : 'halt',
		}

		pos = 0
		while pos < len(self.memory):
			opcode, mode = self.decode_instruction(self.memory[pos], True)
			print(f"[{pos}]\t", end='')
			if opcode in mnemonics:
				print(f"{mnemonics[opcode]} ", end='')
			else:
				print(f"{opcode}", end='')

			for m in range( len(mode) ):
				if mode[m] == 0:
					print(f"${self.memory[ pos + m + 1 ]} ", end='')
				elif mode[m] == 1:
					print(f"{self.memory[ pos + m + 1 ]} ", end='')
				elif mode[m] == 2:
					print(f"$RB+{self.memory[ pos + m + 1 ]} ", end='')

			print()
			pos += 1
			pos += len(mode)



	def pad_memory(self, size, padding = 0):
		while len(self.memory) < size:
			self.memory.append(padding)



def main():
	program = VM(sys.argv[1])
	try:
		if sys.argv[2] == "DEBUG":
			global DEBUG
			DEBUG = True
			program.run()
		elif sys.argv[2] == "DISASM":
			program.disassemble()
		else:
			program.run()
	except:
		program.run()

	

if __name__ == '__main__':
	main()




















