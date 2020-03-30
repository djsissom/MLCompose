#!/usr/bin/env python

import unittest

from mlcompose.util import containers



class InheritanceTestClass1(containers.CheckArg):
	pass



class InheritanceTestClass2(containers.CheckArg):
	def __init__(self, arg):
		print(arg)



class TestMetaClasses(unittest.TestCase):
	def test_passing_existing_instance_of_same_class_as_arg(self):
		a = containers.CheckArg()
		b = containers.CheckArg(a)
		self.assertTrue(a is b)
		return


	def test_passing_existing_instance_of_different_class_as_arg(self):
		a = InheritanceTestClass1()
		b = InheritanceTestClass2(a)
		self.assertTrue(a is not b)
		return



if __name__ == "__main__":
	unittest.main()

