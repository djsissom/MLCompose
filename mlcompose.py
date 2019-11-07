#!/usr/bin/env python

import sys
from ipdb import set_trace
from ipdb import launch_ipdb_on_exception

import config
import music
import learn



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
	# run analysis and create plots to inform model choices
	#===========================================================================
	if settings.mode.analysis:
		# TODO: call analysis launcher function
		pass


	#===========================================================================
	# train a new model or import an existing one
	#===========================================================================
	if settings.mode.import_model:
		# TODO: call import function
		pass

	elif settings.mode.train:
		# TODO: call training function
		pass


	#===========================================================================
	# compose new music with loaded ML model
	#===========================================================================
	if settings.mode.compose:
		# TODO: call the compose function
		pass


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

