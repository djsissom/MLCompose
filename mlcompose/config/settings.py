#!/usr/bin/env python

import sys
import configparser



def main():
	'''
	settings.py

	Provides Settings class for options in configuration file.
	'''

	# get filename of config file
	config_file = 'settings.conf'
	if len(sys.argv) > 1:
		config_file = sys.argv[1]

	# read config file
	settings = Settings(config_file)

	return



class Settings:
	def __init__(self, config_file):
		config = configparser.ConfigParser()
		config.read(config_file)

		self.mode  = self.Section_Settings(config, 'mode')
		self.files = self.Section_Settings(config, 'files')


	class Section_Settings():
		def __init__(self, config, section):
			settings_list = config.items(section)
			settings_list = [self.convert_type(x) for x in settings_list]
			for key, value in settings_list:
				exec('self.' + key + ' = value')


		def convert_type(self, setting):
			key = setting[0]
			value = setting[1]
			if type(value) == str:
				if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
					value = value[1:-1]
				elif value[0] == 'r' and ((value[1] == '"' and value[-1] == '"') or (value[1] == "'" and value[-1] == "'")):
					value = r"%s" % value[2:-1]
				elif value.lower() == 'true' or value.lower() == 'yes' or value.lower() == 'on':
					value = True
				elif value.lower() == 'false' or value.lower() == 'no' or value.lower() == 'off':
					value = False
				elif value.lower() == 'none':
					value = None
				elif '.' in value:
					value = float(value)
				elif value.isdigit():
					value = int(value)
				else:
					raise ValueError(f'Setting "{key}" with value "{value}" was unable to be converted to an appropriate type.')
			else:
				raise ValueError(f'Something went wrong in the config file while reading ({key}, {value}).')

			return (key, value)



if __name__ == "__main__":
	main()

