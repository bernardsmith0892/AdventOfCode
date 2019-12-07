#!/usr/local/bin/python3.7

def calculate_fuel(mass):
	return (mass // 3) - 2;

def calculate_fuel_complete(mass):
	fuel = (mass // 3) - 2;
	total_fuel = 0;

	while(fuel > 0):
		total_fuel += fuel;
		fuel = (fuel // 3) - 2;

	return total_fuel;


def part1():
	sum = 0;
	for mass in open("inputs/day1.txt").readlines():
		sum += calculate_fuel(int(mass));

	print(sum)

def part2():
	sum = 0;
	for mass in open("inputs/day1.txt").readlines():
		sum += calculate_fuel_complete(int(mass));

	print(sum)


def main():
	part1();
	part2();


if __name__ == "__main__":
	main();
