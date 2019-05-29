#!/usr/bin/env python

import sys
from ipdb import set_trace
from ipdb import launch_ipdb_on_exception

import config



def main():
	'''
	mlcompose.py

	Compose music with deep learning.
	'''


	#===========================================================================
	# read command line options and config files
	#===========================================================================
	settings = config.read_configs()


	#===========================================================================
	# finish up
	#===========================================================================
	print("Exiting mlcompose.")
	if settings.mode.debug:
		set_trace()
	return



if __name__ == "__main__":
	with launch_ipdb_on_exception():
		main()

