#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import cycle
from ipdb import set_trace

from .. import util



def main():
	'''
	containers.py

	Formatting and storage for music data.
	'''

	test_song = Song()
	test_track = Track()
	test_measure = Measure()
	test_beat = Beat()
	test_note = Note()
	test_rest = Rest()
	test_event = Event()
	test_control = Control()

	test_song.add_track(test_track)
	test_track.append_measure(test_measure)

	return



class Song():
	def __init__(self, key='C_Maj', time_signature='4/4', settings=None):
		self.settings = settings
		self.key = key
		self.time_signature = time_signature
		self.tracks = []


	def set_timesig(self, timesig):
		self._time_signature = TimeSignature(timesig)
		return


	def get_timesig(self):
		timesig = self._time_signature
		return timesig


	time_signature = property(get_timesig, set_timesig)


	def set_key(self, keysig):
		self._key = Key(keysig)
		return key


	def get_key(self):
		keysig = self._key
		return keysig


	key = property(get_key, set_key)


	def add_track(self, track):
		self.tracks.append(track)
		return self.tracks


	def end_song(self):
		for track in self.tracks:
			track.end_track()
		return



class Track():
	def __init__(self, desc=None):
		self.description = desc
		self.measures = []


	def set_description(self, desc):
		self._description = desc
		return


	def get_description(self):
		return self._description


	description = property(get_description, set_description)


	def append_measure(self, measure):
		self.measures.append(measure)
		return self.measures


	def end_track(self):
		end_signal = Event('end_track')
		self.measures[-1].add_event(end_signal)
		return



class Measure():
	def __init__(self, key=None, time_signature=None):
		self.key = key
		self.time_signature = time_signature
		self.beats = []


	def set_key(self, keysig):
		self._key = Key(keysig)
		return


	def get_key(self):
		keysig = self._key
		return keysig


	key = property(get_key, set_key)


	def set_timesig(self, timesig):
		self._time_signature = TimeSignature(timesig)
		return


	def get_timesig(self):
		timesig = self._time_signature
		return timesig


	time_signature = property(get_timesig, set_timesig)


	def append_beat(self, beat):
		self.beats.append(beat)
		return self.beats



class Beat():
	def __init__(self, offset=1):
		self.offset = offset
		self.notes = []
		self.events = []


	def set_offset(self, offset):
		self._offset = offset
		return


	def get_offset(self):
		offset = self._offset
		return offset


	offset = property(get_offset, set_offset)


	def append_note(self, note):
		self.notes.append(note)
		return self.notes


	def add_event(self, event):
		self.events.append(event)
		return self.events



class Note(util.CheckArg):
	def __init__(self, note=None, name=None, value=None, octave=None, duration=None, intensity=None, tie=None):
		self.sharpnames = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
		self.flatnames  = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
		if (note is None) and (name is None) and (value is None) and (octave is None) \
		                  and (duration is None) and (intensity is None) and (tie is None):
			self.value     = None
			self.duration  = None
			self.intensity = None
			self.tie       = None
		else:
			self.set(note, name, value, octave, duration, intensity, tie)


	def set(self, note=None, name=None, value=None, octave=None, duration=None, intensity=None, tie=None):
		if note is None:
			if value is None:
				if (name is None) or (octave is None):
					raise AttributeError("Must specify either the numerical value or the name and octave of note.")
				else:
					self.name = name
					self.octave = octave
			else:
				self.value = value
		else:
			input_type = type(key)
			case = {
				str: self.parse_string,
				tuple: self.parse_tuple
			}
			parse_func = case.get(input_type)
			value, duration, intensity, tie = parse_func(key)
		self.value = value
		self.duration = duration
		self.intensity = intensity
		self.tie = tie
		return self


	def parse_string(self, note):
		return


	def parse_tuple(self, note):
		return


	def set_value(self, value):
		if (value is not None) and ((value < 0) or (value > 127)):
			raise AttributeError("Note value must be in the range 0-127 (inclusive).")
		self._value = value
		return


	def get_value(self):
		value = self._value
		return value


	value = property(get_value, set_value)


	def set_name(self, name):
		if name in self.sharpnames:
			names = self.sharpnames
		elif name in self.flatnames:
			names = self.flatnames
		else:
			raise AttributeError("Invalid note name supplied.")
		index = names.index(name)
		if self.value is None:
			octave = 0
		else:
			x = self.value
			octave = int(x / 12)
		self._value = index + (12 * octave)
		return


	def get_name(self, enharmonic='sharp'):
		if self.value is None:
			name = None
		else:
			if enharmonic.lower() in ('sharp', 's', '#'):
				names = self.sharpnames
			elif enharmonic.lower() in ('flat', 'f', 'b'):
				names = self.flatnames
			cycleval = self.value
			while cycleval >= 12:
				cycleval = cycleval - 12
			name = names[cycleval]
		return name


	name = property(get_name, set_name)


	def raise_note(self, degree='halfstep'):
		return


	def lower_note(self, degree='halfstep'):
		return


	def raise_octave(self, degree=1):
		return


	def lower_octave(self, degree=1):
		return



class Rest():
	def __init__(self, duration=None):
		self.duration = duration



class Event():
	def __init__(self, event_type=None, descr=None):
		self.event_type = event_type
		self.description = descr



class Key(util.CheckArg):
	'''
	Key(key=None, naccidentals=None, sharpflat=None, majmin=None)

	Create a Key object.  If no parameters are given, creates an uninitialized
	instance.  Can be (re-)initialized with the set() method with the same
	parameters.

	Parameters
	----------
	key : str, tuple, or Key instance (optional)
	naccidentals : int <= 6 (optional)
	sharpflat : {0, 1, -1, 'sharp', 'flat'} (optional)
	majmin: {0, 1, 'major', 'maj', 'minor', 'min'} (optional)
	'''
	def __init__(self, key=None, naccidentals=None, sharpflat=None, majmin=None):
		self.majkeys = ('C', 'G',  'D',  'A',  'E',  'B',  'F#',
		                     'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F')
		self.minkeys = ('A', 'E',  'B',  'F#', 'C#', 'G#', 'D#',
		                     'Eb', 'Bb', 'F',  'C',  'G',  'D')
		self.sharps = ('F', 'C', 'G', 'D', 'A', 'E')
		self.flats =  ('B', 'E', 'A', 'D', 'G', 'C')
		self.allnotes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
		if (key is None) and (naccidentals is None) and (sharpflat is None) and (majmin is None):
			self.naccidentals = None
			self.sharp_flat   = None
			self.major_minor  = None
			self.accidentals  = None
			self.notes        = None
		else:
			self.set(key, naccidentals, sharpflat, majmin)


	def set(self, key=None, naccidentals=None, sharpflat=None, majmin=None):
		if key is None:
			if (naccidentals is None) or (sharpflat is None) or (majmin is None):
				raise AttributeError("Must either specify key or all of naccidentals, sharpflat, and majmin.")
			else:
				naccs = naccidentals
				sf = sharpflat
				mm = majmin
		else:
			input_type = type(key)
			case = {
				str: self.parse_string,
				tuple: self.parse_tuple
			}
			parse_func = case.get(input_type)
			naccs, sf, mm = parse_func(key)
		self.naccidentals = naccs
		self.sharp_flat = sf
		self.major_minor = mm
		self.set_accidentals()
		self.set_notes()
		return self


	def parse_string(self, key):
		mm_string = key[-3:]
		if mm_string.lower() == 'maj':
			mm = 0
			keylist = self.majkeys
		elif mm_string.lower() == 'min':
			mm = 1
			keylist = self.minkeys
		else:
			raise AttributeError("String used to initialize Key class must end in 'Maj', or 'min' (case-insensitive).")

		if (key[1] == 'b') or (key[1] == '#'):
			namelen = 2
		else:
			namelen = 1
		keyname = key[:namelen]
		indexlist = [i for i, x in enumerate(keylist) if x.lower() == keyname.lower()]
		if len(indexlist) == 1:
			index = indexlist[0]
		else:
			print("you passed " + keyname)
			print(indexlist)
			raise AttributeError("%s key name must be one of %s" % (mm_string, str(keylist)))

		if index > 6:
			naccs = len(keylist) - index
			sf = -1
		elif index == 0:
			naccs = 0
			sf = 0
		else:
			naccs = index
			sf = 1

		return naccs, sf, mm


	def parse_tuple(self, key):
		naccs, sf, mm = key[:]
		return naccs, sf, mm


	def set_naccidentals(self, naccs):
		if naccs is not None:
			naccs = int(naccs)
			if naccs > 6:
				raise AttributeError("Specified number of naccidentals must be fewer than 7.")
		self._naccidentals = naccs
		return


	def get_naccidentals(self):
		naccs = self._naccidentals
		return naccs


	n_accidentals = property(get_naccidentals, set_naccidentals)
	naccidentals  = property(get_naccidentals, set_naccidentals)
	n_accs        = property(get_naccidentals, set_naccidentals)
	naccs         = property(get_naccidentals, set_naccidentals)


	def set_sharp_flat(self, sf):
		if type(sf) is str:
			if sf == '0':
				sf = 0
			elif (sf.lower() == 'sharp') or (sf == '1'):
				sf = 1
			elif (sf.lower() == 'flat') or (sf == '-1'):
				sf = -1
		if (sf is None) or (sf == 0) or (sf == 1) or (sf == -1):
			self._sharp_flat = sf
		else:
			raise AttributeError("Option sharpflat must be one of 0, 1, -1, 'sharp', or 'flat'.")
		return


	def get_sharp_flat(self):
		sf = self._sharp_flat
		return sf


	sharp_flat = property(get_sharp_flat, set_sharp_flat)
	sharpflat  = property(get_sharp_flat, set_sharp_flat)
	sf         = property(get_sharp_flat, set_sharp_flat)


	def set_major_minor(self, mm):
		if type(mm) is str:
			if (mm.lower() == 'major') or (mm.lower() == 'maj') or (mm == '0'):
				mm = 0
			elif (mm.lower() == 'minor') or (mm.lower() == 'min') or (mm == '1'):
				mm = 1
		if (mm is None) or (mm == 0) or (mm == 1):
			self._major_minor = mm
		return


	def get_major_minor(self):
		mm = self._major_minor
		return mm


	major_minor = property(get_major_minor, set_major_minor)
	majorminor  = property(get_major_minor, set_major_minor)
	mm          = property(get_major_minor, set_major_minor)


	def set_accidentals(self):
		naccs = self.naccidentals
		sf = self.sharp_flat
		if naccs == 0 and sf == 0:
			self.accidentals = ()
		else:
			if sf == 1:
				acclist = self.sharps
			elif sf == -1:
				acclist = self.flats
			self.accidentals = acclist[:naccs]
		return


	def set_notes(self):
		notecycle = cycle(self.allnotes)
		keyname = str(self)
		basenote = keyname[0]

		nextnote = next(notecycle)
		while basenote != nextnote:
			nextnote = next(notecycle)

		notes = []
		acc_strings = ['', '#', 'b']
		while len(notes) < 7:
			if nextnote in self.accidentals:
				acc_string = acc_strings[self.sharpflat]
				nextnote = nextnote + acc_string
			notes.append(nextnote)
			nextnote = next(notecycle)
		self.notes = tuple(notes)
		return


	def degree_to_note(self, degree):
		# scale degrees start at 1
		note = self.notes[degree-1]
		return note


	def note_to_degree(self, note):
		# scale degrees start at 1
		note = str(note)
		if note in self.notes:
			degree = self.notes.index(note) + 1
		else:
			raise AttributeError("Provided note is not in the key.")
		return degree


	def __str__(self):
		naccs = self.naccidentals
		sf = self.sharp_flat
		mm = self.major_minor
		if (naccs is not None) and (sf is not None) and (mm is not None):
			keylist = (self.majkeys, self.minkeys)[mm]
			mm_string = ('_Maj', '_min')[mm]
			repstring = keylist[sf * naccs] + mm_string
		else:
			repstring = 'Uninitialized time signature'
		return repstring



class TimeSignature(util.CheckArg):
	'''
	TimeSignature class to handle formatting and saving time signature
	representations.  The optional timesig argument can be a length-2 tuple
	containing the numerator and denominator of the time signature, a string
	containing the numerator and denominator separated by one of '/', '-', '_',
	'.', ',', or ' ', or an existing instance of the class.  The respective
	properties can be accessed via the numerator or denominator attributes or
	by casting the instance to a string.
	'''
	def __init__(self, timesig=None):
		self.numerator = None
		self.denominator = None
		if timesig is not None:
			self.set(timesig)


	def set(self, timesig):
		input_type = type(timesig)
		case = {
			str: self.parse_string,
			tuple: self.parse_tuple
		}
		parse_func = case.get(input_type)
		numerator, denominator = parse_func(timesig)
		self.numerator = numerator
		self.denominator = denominator
		return self


	def parse_string(self, timesig):
		delimiters = ['/', '-', '_', '.', ',', ' ']
		if any(delimiter in timesig for delimiter in delimiters):
			for delimiter in delimiters:
				if delimiter in timesig:
					timesig_tuple = timesig.split(delimiter)
					numerator, denominator = self.parse_tuple(timesig_tuple)
					break
		else:
			raise AttributeError("Available TimeSignature string delimiters: '" \
				+ "', '".join(delimiters) + "'")
		return numerator, denominator


	def parse_tuple(self, timesig):
		if len(timesig) == 2:
			numerator = int(timesig[0])
			denominator = int(timesig[1])
		else:
			raise AttributeError( \
				"Setting TimeSignature with tuple requires a length 2 tuple.")
		return numerator, denominator


	def __str__(self):
		numer = self.numerator
		denom = self.denominator
		if (numer is not None) and (denom is not None):
			repstring = str(numer) + '/' + str(denom)
		else:
			repstring = 'Uninitialized time signature'
		return repstring



class Control():
	def __init__(self, song=None):
		# set default song to work on
		self.song = song

		# tensor of nodes from neural net output
		self.nodes = np.zeros((6,8), dtype=np.float)

		# Array slices are used to make view instead of copy.  Descriptive
		# names can then be used to reference node values without
		# reinitialization steps.

		# first row used for mode control toggles
		self.modecontrol_nodes    = self.nodes[0,:]
		self.mode_nodes           = self.nodes[0,0:3]
		self.controloption_nodes  = self.nodes[0,3:8]

		self.endsong_node         = self.nodes[0,0:1]
		self.notemode_node        = self.nodes[0,1:2]
		self.controlmode_node     = self.nodes[0,2:3]
		self.change_keysig_node   = self.nodes[0,3:4]
		self.change_timesig_node  = self.nodes[0,4:5]
		self.change_tempo_node    = self.nodes[0,5:6]
		self.change_dynamic_node  = self.nodes[0,6:7]
		self.pedal_toggle_node    = self.nodes[0,7:8]

		# note mode needs note value, octave, and length
		self.rest_node            = self.nodes[1,0:1]
		self.note_nodes           = self.nodes[1,:]      # cyclical
		self.octave_nodes         = self.nodes[2,:]      # linear
		self.duration_nodes       = self.nodes[3,0:6]    # linear
		self.tie_nodes            = self.nodes[3,6:8]    # on/off

		# last two rows used for other per note settings
		self.note_settings_nodes  = self.nodes[4:6,:]

		self.accidental_nodes     = self.nodes[4,0:3]    # flat, natural (no change), sharp
		self.accent_nodes         = self.nodes[4,3:5]    # on/off
		self.arpeggio_nodes       = self.nodes[4,5:8]    # off/up/down
		self.velocity_nodes       = self.nodes[5,0:6]    # linear
		self.hand_nodes           = self.nodes[5,6:8]    # left/right

		# settings for control modes
		self.keysig_nodes         = self.nodes[1,:]
		self.keysig_sf_nodes      = self.nodes[4,0:3]
		self.timesig_numer_nodes  = self.nodes[2:4,:]
		self.timesig_denom_nodes  = self.nodes[5,:]
		self.tempo_nodes          = self.nodes[4:6,:]
		self.dynamic_nodes        = self.nodes[5,0:6]
		### ### ### ###


	def set_song(self, song):
		self._song = song
		return


	def get_song(self, song=None):
		if song == None:
			song = self._song
		return song


	song = property(get_song, set_song)


	def update(self, song=None):
		song = self.get_song(song)

		max_mode_index = self.mode_nodes.argmax()
		mode_functions = [
			self.end_song,
			self.make_note,
			self.set_control_signal
		]
		mode_function = mode_functions[max_mode_index]
		return mode_function(song)


	def update_altmethod(self, song=None):
		song = self.get_song(song)

		if (endsong_node > notemode_node) and \
		   (endsong_node > controlmode_node):
			return self.end_song(song)
		elif (notemode_node >= endsong_node) and \
		     (notemode_node >= controlmode_node):
			return self.make_note(song)
		elif (controlmode_node >= endsong_node) and \
		     (controlmode_node > notemode_node):
			return self.set_control_signal(song)
		else:
			print("Shouldn't get here...")
			sys.exit(1923485)
		return


	def end_song(self, song=None):
		song = self.get_song(song)
		return


	def make_note(self, song=None, key='C_Maj'):
		song = self.get_song(song)
		if song == None:
			song = self.song

		note_index = self.note_nodes.argmax()
		if note_index == 0:
			self.set_rest()
		else:
			scale_degree = note_index

		note = Note(degree=scale_degree, octave=octave, \
		            duration=duration, intensity=intensity, \
					tie=tie)
		return note


	def set_rest(self, song=None):
		song = self.get_song(song)
		return


	def set_control_signal(self, song=None):
		song = self.get_song(song)
		return



if __name__ == "__main__":
	main()

