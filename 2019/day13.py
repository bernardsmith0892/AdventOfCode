#!/usr/local/bin/python3.7

import Intcode
from PIL import Image, ImageDraw, ImageFont
import os

''' Prints an image of the current arcade tiles '''
def print_arcade(tiles):
	os.system('clear')
	tile_types = {
	0 : ' ',
	1 : '░',
	2 : '█',
	3 : '▄',
	4 : 'o'
	}

	max_x = 0
	max_y = 0

	for pos in tiles.keys():
		x = int(pos.split(',')[0])
		y = int(pos.split(',')[1])

		max_x = x if x > max_x else max_x
		max_y = y if y > max_y else max_y

	for y in range(max_y + 1):
		for x in range(max_x + 1):
			print(f"{tile_types[ tiles[f'{x},{y}'] ]}", end='')
		print()

	if '-1,0' in tiles.keys():
		print(f"Score: {tiles['-1,0']}")
		if int(tiles['-1,0']) > 5000:
			global slow
			slow = True

''' Returns an image of the current arcade tiles '''
def draw_arcade(tiles):
	pixel_size = 10
	tile_types = {
		0 : 'white',
		1 : 'grey',
		2 : 'blue',
		3 : 'red',
		4 : 'orange'
	}

	max_x = 0
	max_y = 0
	for pos in tiles.keys():
		x = int(pos.split(',')[0])
		y = int(pos.split(',')[1])

		max_x = x if x > max_x else max_x
		max_y = y if y > max_y else max_y


	img = Image.new('RGB', (max_x * pixel_size + pixel_size, max_y * pixel_size + pixel_size * 2), (255,255,255))
	draw = ImageDraw.Draw(img)

	for y in range(0, max_y + 1):
		for x in range(max_x + 1):
			color = tile_types[ tiles[f'{x},{y}'] ]
			draw.rectangle([x*pixel_size, (y+1)*pixel_size, x*pixel_size + pixel_size, (y+1)*pixel_size + pixel_size], fill=color)
	
	font = ImageFont.truetype("/Library/Fonts/Arial.ttf")
	draw.text([0,-1], f"Score: {tiles['-1,0']}", fill='black', font=font)
	return img

''' Returns the coordinates of the ball and paddle '''
def find_ball_and_paddle(tiles):
	ball = [0,0]
	paddle = [0,0]

	for i in tiles.items():
		if i[1] == 3:
			paddle = [int(i[0].split(',')[0]),int(i[0].split(',')[1])]
		elif i[1] == 4:
			ball = [int(i[0].split(',')[0]),int(i[0].split(',')[1])]

	return ball, paddle

def main():
	arcade = Intcode.VM('inputs/day13.txt', automated=True)

	tiles = {}
	status = arcade.step()
	gif = []
	ball = [0,0]
	paddle = [0,0]
	frame_save = 0

	print("Running Game...")
	while status != False:
		if status == None:
			ball, paddle = find_ball_and_paddle(tiles)

			if ball[0] > paddle[0]:
				control = 1
			elif ball[0] < paddle[0]:
				control = -1
			elif int(ball[1]) >= 19:
				control = 0
			else:
				control = 0

			'''
			input_good = False
			while input_good == False:
				print_arcade(tiles)
				control = input("Move (-1 : 0 : 1): ")
				input_good = True
				if control == '':
					control = 0
				elif control != '-1' and control != '0' and control != '1':
					input_good = False
			'''
			arcade.add_to_input_queue(control)

			#print_arcade(tiles)
			#print(f"Ball X: {ball[0]}, Paddle X: {paddle[0]}")
			#print(f"Velocity: {ball_velocity}, Ball Y: {ball[1]}")
			#if slow:
			#	input("...")
			if frame_save == 0:
				img = draw_arcade(tiles)
				gif.append(img)
				frame_save = (frame_save + 1) % 4
			else:
				frame_save = (frame_save + 1) % 4
			#img.save('arcade.png', 'PNG')
			

		while len(arcade.output_queue) >= 3:
			x = arcade.read_from_output_queue()
			y = arcade.read_from_output_queue()
			tile_id = arcade.read_from_output_queue()

			tiles[f"{x},{y}"] = tile_id

		status = arcade.step()

	print_arcade(tiles)
	print("Creating GIF...")
	gif[0].save('arcade.gif', format='GIF', append_images=gif[1:], save_all=True, loop=1)

if __name__ == '__main__':
	main()
