#!/usr/bin/env python

import sys



def main():
	'''
	containers.py

	Container base classes.
	'''

	print()
	print("Creating object a...")
	a = ArgSelfCheck()
	b = ArgSelfCheck(a)
	print(b is a)

	return



class _MetaCheckArg(type):
	'''
	Metaclass to implement actual CheckArg functionality.  Actual CheckArg
	class is provided to not have to worry about including 'metaclass=' in
	class inheritance for new subclasses.
	'''
	def __call__(cls, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0], cls):
			return args[0]
		instance = cls.__new__(cls)
		instance.__init__(*args, **kwargs)
		return instance



class CheckArg(metaclass=_MetaCheckArg):
	'''
	Inheriting from CheckArg class provides built in handling to check if an
	already created instance of a class is passed as the argument when creating
	a new instance.  If so, the argument (the already existing instance) is
	returned instead of creating an actual new instance.  Otherwise, a new
	instance is created as normal with arguments passed to __init__.
	'''
	pass



if __name__ == "__main__":
	main()

