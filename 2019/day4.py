#!/usr/local/bin/python3.7

def validate_password(password):
	double = False

	hold_num = password[0]
	for num in password[1:]:
		if num == hold_num:
			double = True
		elif num < hold_num:
			return False
		hold_num = num

	return double

def validate_password_v2(password):
	repeated = 0
	double = False
	hold_num = password[0]

	for num in password[1:]:
		if num < hold_num:
			return False
		elif num == hold_num:
			repeated += 1
		elif num != hold_num:
			if repeated == 1:
				double = True
			repeated = 0
		
		hold_num = num

	if repeated == 1:
		double = True

	return double




valid_passwords = 0
for num in range(136760, 595730 + 1):
	if validate_password_v2(str(num)):
		valid_passwords += 1

print(valid_passwords)
