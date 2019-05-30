#!/usr/bin/env python

import numpy as np
import pandas as pd
from ipdb import set_trace



def main():
	'''
	containers.py

	Formatting and storage for music data.
	'''

	return



class Song():
	def __init__(self, key='C_Maj', time_signature=None, settings=None):
		self.settings = settings
		self.key = key
		self.time_signature = time_signature


	def add_note(self, note):
		return



class Note():
	def __init__(self, value=None, octave=None, duration=None, intensity=None, tie=None):
		self.value = value
		self.octave = octave
		self.duration = duration
		self.intensity = intensity
		self.tie = tie



class Note_Nodes():
	def __init__(self, value=None, octave=None, duration=None, intensity=None, tie=None):
		self.value = value
		self.octave = octave
		self.duration = duration
		self.intensity = intensity
		self.tie = tie



if __name__ == "__main__":
	main()

