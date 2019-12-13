#!/usr/local/bin/python3.7

import Intcode

panels = {}
robot = Intcode.VM("inputs/day11.txt", size = 2056, automated = True)
direction = 0
x,y = 0,0

def run_robot(x, y, direction, panels, robot):
	status = True
	output_expecting_color = True
	panels[f"{x},{y}"] = 1

	while status != False:
		if status == None: # Add current color to the queue if the bot is waiting for input
			current_color = 0 if (f"{x},{y}" not in panels) else panels[f"{x},{y}"]
			robot.add_to_input_queue(current_color)
		elif robot.output_in_queue():
			if output_expecting_color: # Paint color
				color = robot.read_from_output_queue()
				panels[f"{x},{y}"] = color

				output_expecting_color = False
			else: 
				# Turn left or right depending on robot input
				turn = robot.read_from_output_queue()
				if turn == 0: # 0 - Up, 1 - Right, 2 - Down, 3 - Left
					direction = (direction - 1) % 4
				else:
					direction = (direction + 1) % 4

				# Move in that direction
				if direction == 0:
					y += 1
				elif direction == 2:
					y -= 1
				elif direction == 1:
					x += 1
				elif direction == 3:
					x -= 1

				output_expecting_color = True

		status = robot.step()

	return panels

def print_panels(panels):
	min_x, max_x = 0,0
	min_y, max_y = 0,0

	for pos in panels.keys():
		x = int(pos.split(',')[0])
		y = int(pos.split(',')[1])

		min_x = x if x < min_x else min_x
		max_x = x if x > max_x else max_x
		min_y = y if y < min_y else min_y
		max_y = y if y > max_y else max_y

	for x in range(min_x, max_x + 1):
		for y in range(min_y, max_y + 1):
			if f"{x},{y}" in panels:
				color = ' ' if panels[f"{x},{y}"] == 0 else '█'
			else:
				color = ' '
			print(color, end='')
		print()

panels = run_robot(x, y, direction, panels, robot)

print_panels(panels)
print(len(panels))




