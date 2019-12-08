#!/usr/local/bin/python3.7

def split_layers(image_data, w, h):
	length = w * h
	layers = []

	start = 0
	stop = length

	while stop <= len(image_data):
		layers.append( image_data[start : stop] )

		start = stop
		stop += length

	return layers

def main():
	data = open("inputs/day8.txt", "r").readline().strip()

	layers = split_layers(data, 25, 6)

	# Part 1
	min_zero = 0, None
	for l in layers:
		current_zero = l.count('0')
		min_zero = (current_zero, l) if  min_zero[1] == None or current_zero < min_zero[0] else min_zero

	print(min_zero[1].count('1') * min_zero[1].count('2'))

	# Part 2
	flat_image = []
	for i in range( 25 * 6 ):
		found_opaque = False
		for l in layers:
			if l[i] == '0' or l[i] == '1':
				flat_image.append( '█' if l[i] == '0' else '░' )
				found_opaque = True
				break

		if not found_opaque:
			flat_image.append(' ')

	for row in range(6):
		print("".join(flat_image[25 * row : 25 * row + 25]))


main()
