#!/usr/local/bin/python3.7

import hashlib

def test_answer(key, num):
	hash_val = hashlib.md5(f'{key}{num}'.encode('utf-8')).hexdigest()
	return hash_val[:5] == "00000"

def test_answer_v2(key, num):
	hash_val = hashlib.md5(f'{key}{num}'.encode('utf-8')).hexdigest()
	return hash_val[:6] == "000000"

def part1():
	num = 1
	key = "bgvyzdsv"
	while not test_answer(key, num):
		num += 1

	print(f"{num} : {hashlib.md5(f'{key}{num}'.encode('utf-8')).hexdigest()}")

def part2():
	num = 1
	key = "bgvyzdsv"
	while not test_answer_v2(key, num):
		num += 1

	print(f"{num} : {hashlib.md5(f'{key}{num}'.encode('utf-8')).hexdigest()}")



part2()