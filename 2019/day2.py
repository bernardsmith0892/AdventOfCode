#!/usr/local/bin/python3.7

def add_instr(a, b, out, cmd_strip):
	cmd_strip[out] = cmd_strip[a] + cmd_strip[b]
	return cmd_strip

def multiply_instr(a, b, out, cmd_strip):
	cmd_strip[out] = cmd_strip[a] * cmd_strip[b]
	return cmd_strip

def run_program(noun, verb):
	cmd_strip = open("day2.txt", "r").readline().split(',')
	cmd_strip = list(map(int, cmd_strip))

	cmd_strip[1] = noun
	cmd_strip[2] = verb

	pos = 0
	while pos < len(cmd_strip):
		if cmd_strip[pos] == 1:
			add_instr(cmd_strip[pos + 1], cmd_strip[pos + 2], cmd_strip[pos + 3], cmd_strip)
			pos += 4
		elif cmd_strip[pos] == 2:
			multiply_instr(cmd_strip[pos + 1], cmd_strip[pos + 2], cmd_strip[pos + 3], cmd_strip)
			pos += 4
		elif cmd_strip[pos] == 99:
			return cmd_strip[0]
		else:
			print(f"ERROR! Unknown opcode {cmd_strip[pos]}")
			break

def part2():
	for noun in range(0, 100):
		for verb in range(0, 100):
			result = run_program(noun, verb)
			if result == 19690720:
				print(f"Noun: {noun}, Verb: {verb}")
				print(f"Answer: {100 * noun + verb}")
				return 100 * noun + verb

# Part 1
print(run_program(12, 2))

part2()



