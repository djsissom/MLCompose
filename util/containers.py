#!/usr/bin/env python

import sys



def main():
	'''
	containers.py

	Container base classes.
	'''

	argselfcheck1 = ArgSelfCheck()
	argselfcheck2 = ArgSelfCheck(argselfcheck1)
	print(argselfcheck1 is argselfcheck2)

	return



class ArgSelfCheck():
	def __new__(cls, *args, **kwargs):
		if (len(args) == 1) and isinstance(args[0], cls):
			return args[0]
		if (len(kwargs) == 1):
			firstval = list(kwargs.values())[0]
			if isinstance(firstval, cls):
				return firstval
		instance = super().__new__(cls)
		instance.init(*args, **kwargs)
		return instance


	def init(self, *args, **kwargs):
		pass



if __name__ == "__main__":
	main()

