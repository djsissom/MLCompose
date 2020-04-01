#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import cycle
from ipdb import set_trace

from . import convert
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

	test_song.add_track(test_track)
	test_track.append_measure(test_measure)

	return



class Song():
	def __init__(self, key='C_Maj', time_signature='4/4', settings=None):
		self.settings = settings
		self.key = key
		self.time_signature = time_signature
		self.tracks = []
		self.ended = False


	def set_timesig(self, timesig):
		self._time_signature = TimeSignature(timesig)
		return


	def get_timesig(self):
		timesig = self._time_signature
		return timesig


	time_signature = property(get_timesig, set_timesig)


	def set_key(self, keysig):
		self._key = Key(keysig)
		return


	def get_key(self):
		keysig = self._key
		return keysig


	key = property(get_key, set_key)


	def add_track(self, track=None):
		if track is None:
			track = Track()
		self.tracks.append(track)
		return track


	def end_song(self):
		for track in self.tracks:
			track.end_track()
		self.ended = True
		return self


	def from_midi(self, midi_file):
		tmp_song = convert.midi_to_song(midi_file)
		self.time_signature = tmp_song.time_signature
		self.key = tmp_song.key
		self.tracks = tmp_song.tracks
		return self


	def to_midi(self, midi_file):
		pattern = convert.song_to_midi(self, midi_file)
		return pattern



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


	def append_measure(self, measure=None):
		if measure is None:
			measure = Measure()
		self.measures.append(measure)
		return measure


	def end_track(self):
		end_signal = Event('end_track')
		self.measures[-1].beats[-1].add_event(end_signal)
		final_measure = self.append_measure()
		final_beat = final_measure.append_beat()
		final_beat.add_event(end_signal)
		return self



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


	def append_beat(self, beat=None):
		if beat is None:
			if self.beats == []:
				beat = Beat(offset=0)
			else:
				beat = Beat()
		self.beats.append(beat)
		return beat



class Beat():
	def __init__(self, offset='quarter'):
		self.offset = offset
		self.notes = []
		self.events = []


	def set_offset(self, offset):
		offset = Duration(offset)
		self._offset = offset
		return


	def get_offset(self):
		offset = self._offset
		return offset


	offset = property(get_offset, set_offset)


	def add_note(self, note):
		self.notes.append(note)
		return note


	def add_event(self, event):
		self.events.append(event)
		return event



class Note(util.CheckArg):
	def __init__(self, note=None, octave=5, duration='quarter', intensity=1.0, tie=False, enharmonic=None, name=None, value=None):
		self.sharpnames = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
		self.flatnames  = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
		self._value = None
		if (note is None) and (name is None) and (value is None):
			self.value      = None
			self.duration   = duration
			self.intensity  = intensity
			self.tie        = tie
			self.enharmonic = enharmonic
		else:
			self.set(note, octave, duration, intensity, tie, enharmonic, name, value)


	def set(self, note=None, octave=5, duration='quarter', intensity=1.0, tie=False, enharmonic=None, name=None, value=None):
		self.duration   = duration
		self.intensity  = intensity
		self.tie        = tie
		self.enharmonic = enharmonic

		if note is not None:
			input_type = type(note)
			case = {
				int: self.parse_int,
				str: self.parse_string,
				tuple: self.parse_tuple
			}
			parse_func = case.get(input_type)
			note, tmp_octave = parse_func(note)
			if type(note) is str:
				name = note
			elif type(note) is int:
				value = note

			if tmp_octave is not None:
				octave = tmp_octave

		if value is None:
			if name is None:
				raise AttributeError("Must specify either the note name or numerical value.")
			else:
				self.name = name
				self.octave = octave
		else:
			if value < 12:
				value = value + (12 * octave)
			self.value = value

		return self


	def parse_int(self, note):
		value = note
		return value, None


	def parse_string(self, note):
		name = note
		octave = None
		for sep in (':', '-', '_'):
			if sep in note:
				name, octave = note.split(sep)
				octave = int(octave)
		return name, octave


	def parse_tuple(self, note):
		if len(note) == 2:
			octave = note[1]
			note = note[0]
		elif len(note) == 1:
			note = note[0]
			octave = None
		else:
			raise AttributeError("Tuples passed as note argument should be length 1 or 2.")

		input_type = type(note)
		case = {
			int: self.parse_int,
			str: self.parse_string
		}
		parse_func = case.get(input_type)
		note, tmp_octave = parse_func(note)
		if octave is None:
			octave = tmp_octave
		return note, octave


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
		en = self.enharmonic
		if (name in self.sharpnames) or (name in self.flatnames):
			if (name in self.sharpnames) and ((en is None) or (en.lower() in ('sharp', 's', '#'))):
				names = self.sharpnames
				if en is None:
					self.enharmonic = 'sharp'
			elif (name in self.flatnames) and ((en is None) or (en.lower() in ('flat', 'f', 'b'))):
				names = self.flatnames
				if en is None:
					self.enharmonic = 'flat'
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


	def get_name(self, enharmonic=None):
		if self.value is None:
			name = None
		else:
			if enharmonic is None:
				enharmonic = self.enharmonic

			if (enharmonic is None) or (enharmonic.lower() in ('sharp', 's', '#')):
				names = self.sharpnames
			elif enharmonic.lower() in ('flat', 'f', 'b'):
				names = self.flatnames

			cycleval = self.value
			while cycleval >= 12:
				cycleval = cycleval - 12
			name = names[cycleval]
		return name


	name = property(get_name, set_name)


	def set_octave(self, octave):
		value = self.value
		old_octave = self.octave
		octave_diff = int(octave) - old_octave
		self.value = value + (12 * octave_diff)
		return


	def get_octave(self):
		value = self.value
		octave = int(value / 12)
		return octave


	octave = property(get_octave, set_octave)


	def set_duration(self, duration):
		duration = Duration(duration)
		self._duration = duration
		return


	def get_duration(self):
		return self._duration


	duration = property(get_duration, set_duration)


	def set_intensity(self, intensity):
		if (intensity < 0) or (intensity > 1):
			raise AttributeError("Intensity should be within the interval [0,1] (inclusive).")
		self._intensity = intensity
		return


	def get_intensity(self):
		return self._intensity


	intensity = property(get_intensity, set_intensity)


	def set_tie(self, tie):
		if type(tie) is not bool:
			if str(tie).lower() in ('true', 't', 'yes', 'y', '1', 'on'):
				tie = True
			elif str(tie).lower() in ('false', 'f', 'no', 'n', '0', 'off'):
				tie = False
			else:
				raise AttributeError("Unable to parse 'tie' option.")
		self._tie = tie
		return


	def get_tie(self):
		return self._tie


	tie = property(get_tie, set_tie)


	def set_enharmonic(self, enharmonic):
		if enharmonic is not None:
			if enharmonic.lower() in ('sharp', 's', '#'):
				enharmonic = 'sharp'
			elif enharmonic.lower() in ('flat', 'f', 'b'):
				enharmonic = 'flat'
			else:
				raise AttributeError("Unable to parse 'enharmonic' option.")
		self._enharmonic = enharmonic
		return


	def get_enharmonic(self):
		return self._enharmonic


	enharmonic = property(get_enharmonic, set_enharmonic)


	def raise_note(self, degree='halfstep'):
		degree = self.parse_step_degree(degree)
		value = self.value
		value = value + degree
		self.value = value
		return


	def lower_note(self, degree='halfstep'):
		degree = self.parse_step_degree(degree)
		value = self.value
		value = value - degree
		self.value = value
		return


	def parse_step_degree(self, degree):
		if degree.lower() == 'halfstep':
			degree = 1
		elif degree.lower() == 'wholestep':
			degree = 2
		if type(degree) is not int:
			raise AttributeError("Degree must be 'halfstep', 'wholestep', or integer number of halfsteps.")
		return degree


	def raise_octave(self, degree=1):
		octave = self.octave
		octave = octave + degree
		self.octave = octave
		return


	def lower_octave(self, degree=1):
		octave = self.octave
		octave = octave - degree
		self.octave = octave
		return


	def __str__(self):
		repstring = self.name + '_' + str(self.octave)
		return repstring



class Rest():
	def __init__(self, duration=None):
		self.duration = duration


	def set_duration(self, duration):
		duration = Duration(duration)
		self._duration = duration
		return


	def get_duration(self):
		return self._duration


	duration = property(get_duration, set_duration)



class Event():
	def __init__(self, name=None, descr=None):
		self.name = name
		self.description = descr



class Duration(util.CheckArg):
	'''
	Duration(base=None, mode='inverse', dot=False)

	Create a Duration object.  If no parameters are given, creates an
	uninitialized instance.  Can be (re-)initialized with the set() method with
	the same parameters.

	Parameters
	----------
	base : str, int power of 2 <= 64, int <= 6, or Duration instance (optional)
		The note or rest duration base.  If a string is passed, allowed names
		are English note names between 'whole' and 'sixty-fourth', optionally
		prepended with 'dotted ' to override and enable the dot option, for
		example: 'dotted thirty-second'.  If an integer is passed, allowed
		values are powers of 2 between 1 and 64 if mode is 'inverse' or
		integers between 0 and 6 if mode is 'inverse_power'.  The special case
		of a zero-length duration is created by setting base to 'zero' or 0
		with mode set to the default 'inverse'.  If an existing Duration object
		is given, setup is skipped and that object is returned.
	mode : {'inverse', 'inverse_power'} (optional)
		Select between specifying the base as a power of two directly
		('inverse') or the exponent with which to raise 2 ('inverse_power').
		This option is ignored if base is a string.
	dot : bool (optional)
		Specify whether the duration should be dotted.  If True, the base duration
		is multiplied by 1.5 (e.g., a dotted quarter is three eighths).
	'''
	def __init__(self, base=None, mode='inverse', dot=False):
		self.names = ['whole', 'half', 'quarter', 'eighth', 'sixteenth', 'thirty-second', 'sixty-fourth', 'zero']
		self.bases = [1, 2, 4, 8, 16, 32, 64, 0]
		self.base = None
		self.dot = None
		if base is not None:
			self.set(base, mode, dot)


	def set(self, base, mode='inverse', dot=False):
		if (type(base) == str) and (base[:6].lower() == 'dotted'):
			dot = True
			base = base[7:]
		# TODO:  Some of this logic could probably move to set_base()
		if (type(base) == str) and (base.lower() in self.names):
			list_index = self.names.index(base.lower())
			self.base = self.bases[list_index]
		elif mode == 'inverse':
			self.base = base
		elif mode == 'inverse_power':
			self.base = 2**base
		else:
			raise AttributeError("Duration class mode options are 'inverse' and 'inverse_power'.")
		self.dot = dot
		return self


	def set_base(self, base):
		if (base not in self.bases) and (base is not None):
			raise AttributeError("Duration base must be a power of 2 between 1 and 64.")
		self._base = base
		return


	def get_base(self):
		return self._base


	base = property(get_base, set_base)


	def set_dot(self, dot):
		if (type(dot) is not bool) and (dot is not None):
			raise AttributeError("Duration class dot attribute must be True or False.")
		self._dot = dot
		return


	def get_dot(self):
		return self._dot


	dot = property(get_dot, set_dot)


	def __str__(self):
		list_index = self.bases.index(self.base)
		basename = self.names[list_index]
		if self.dot:
			repstring = 'dotted ' + basename
		else:
			repstring = basename
		return repstring



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



if __name__ == "__main__":
	main()

