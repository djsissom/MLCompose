#!/usr/bin/env python

import sys
import getopt
import textwrap



def main():
	'''
	opts.py

	Read flags and options provided on the command line.
	'''

	# read command line options
	opts = Opts(sys.argv[1:])

	return



class Opts:
	def __init__(self, optlist):
		self.help_string = textwrap.dedent('''\
		Available options are:
			-h, --help     :  print this message
			-v, --verbose  :  output more status information
			-d, --debug    :  run in debug mode
			-c <configfile>, --config <configfile>   :  specify configuration file (defaults to settings.conf)\
		''')
		self.shortopts = "hvdc:"
		self.longopts  = ["help", "verbose", "debug", "config="]

		self.verbose         =  False
		self.debug           =  False
		self.config_file     =  None
		self.mlcompose_files  =  None

		opts, args = self.get_opts_args(optlist)
		self.parse_opts_args(opts, args)


	def get_opts_args(self, optlist):
		try:
			opts, args = getopt.gnu_getopt(optlist, self.shortopts, self.longopts)
		except getopt.GetoptError:
			print("Invalid option(s).")
			print(self.help_string)
			sys.exit(2)

		return opts, args


	def parse_opts_args(self, opts, args):
		for opt in opts:
			if (opt[0] == '-h') or (opt[0] == '--help'):
				print(self.help_string)
				sys.exit(0)
			elif (opt[0] == '-v') or (opt[0] == '--verbose'):
				self.verbose = True
			elif (opt[0] == '-d') or (opt[0] == '--debug'):
				self.debug = True
			elif (opt[0] == '-c') or (opt[0] == '--config'):
				self.config_file = opt[1]
			else:
				print("Invalid option(s).")
				print(self.help_string)
				sys.exit(2)
		if args is not None:
			self.mlcompose_files = args
		return


	def override_settings(self, settings):
		if self.verbose:
			settings.verbose = True
		if self.debug:
			settings.debug = True
		return settings



if __name__ == "__main__":
	main()

