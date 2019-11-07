#!/usr/bin/env python

import sys
import config



def main():
	'''
	util.py

	Helper function(s) for config setup.
	'''

	# read command line options
	settings = read_configs()

	return



def read_configs():
	# get command line options and filenames
	config_file = 'settings.conf'
	opts = None
	if len(sys.argv) > 1:
		opts = config.Opts(sys.argv[1:])
		if opts.config_file != None:
			config_file = opts.config_file

	# read config file
	settings = config.Settings(config_file)

	if opts != None:
		opts.override_settings(settings)
		if opts.mlcompose_files is not None:
			settings.files.mlcompose_files = opts.mlcompose_files

	return settings



if __name__ == "__main__":
	main()

