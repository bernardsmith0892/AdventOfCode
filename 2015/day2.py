#!/usr/local/bin/python3.7

data = open("inputs/day2.txt", "r").readlines()

def surface_area(l, w, h):
	area = 2*l*w + 2*w*h + 2*h*l
	if l*w < w*h and l*w < h*l:
		area += l*w
	elif w*h < h*l:
		area += w*h
	else:
		area += h*l

	return area

def ribbon_length(l, w, h):
	length = l * w * h

	if l*w < w*h and l*w < h*l:
		length += l + l + w + w
	elif w*h < h*l:
		length += w + w + h + h
	else:
		length += h + h + l + l

	return length

def part1():
	total_paper = 0
	for box in data:
		l, w, h = box.split('x')
		total_paper += surface_area(int(l), int(w), int(h))

	print(total_paper)

def part2():
	total_paper = 0
	for box in data:
		l, w, h = box.split('x')
		total_paper += ribbon_length(int(l), int(w), int(h))

	print(total_paper)


part1()
part2()