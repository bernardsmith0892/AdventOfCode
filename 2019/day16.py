#!/usr/local/bin/python3.7

import time

def FFT(input_list, pattern, phases=1):
	mod = len(pattern)

	while phases > 0:
		output = []
		for out_char in range( len(input_list) ):
			p = 1
			char_value = 0

			for i in input_list:
				char_value += i * pattern[ (p % (mod * (out_char + 1)) ) // (out_char + 1) ]
				p += 1
			output.append(abs(char_value) % 10)

		input_list = output
		phases -= 1

	return output

def FFTv2(input_list, offset, phases=1):
	input_list = input_list[offset:]
	print(len(input_list))
	while phases > 0:
		print(f" Phase: {phases}  ", end="\r")
		output = []
		total_sum = 0
		for i in input_list:
			total_sum += i

		for i in input_list:
			output.append(total_sum % 10)
			total_sum -= i
			

		input_list = output
		phases -= 1

	print()
	return output

def main():
	with open("inputs/day16.txt", "r") as data:
		input_list = data.readline().strip()
		input_list = input_list * 10000
		input_list = list(map(int, input_list))

		print(len(input_list))
		output_data = FFTv2(input_list, 5970837, 100)

		print(len(output_data))
		print("".join( list(map(str,output_data[:8])) ))

if __name__ == "__main__":
	main()