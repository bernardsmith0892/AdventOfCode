#!/usr/local/bin/python3.7

words = open("inputs/day5.txt", "r").readlines()

def vowels_test(word):
	vowels = "aeiou"
	matches = 0

	for c in word:
		if c in vowels:
			matches += 1

	return matches >= 3

def repeat_test(word):
	hold_char = ''

	for c in word:
		if c == hold_char:
			return True
		hold_char = c

	return False

def bad_str_test(word):
	bad_str = ['ab', 'cd', 'pq', 'xy']

	for bs in bad_str:
		if bs in word:
			return False

	return True

def double_repeat_test(word):
	hold_str = word[:2]

	for i in range(2, len(word) ):
		if hold_str in word[i:]:
			return True

		hold_str = hold_str[1] + word[i]

	return False

def repeat_split_test(word):
	hold_char = word[0]
	split_char = word[1]

	for c in word[2:]:
		if hold_char == c:
			return True

		hold_char = split_char
		split_char = c

	return False

def part1():
	nice_strs = 0
	for w in words:
		if vowels_test(w) and repeat_test(w) and bad_str_test(w):
			nice_strs += 1
	print(nice_strs)

def part2():
	nice_strs = 0
	for w in words:
		if double_repeat_test(w) and repeat_split_test(w):
			nice_strs += 1
	print(nice_strs)

part1()
part2()