#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import cycle

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
	# TODO:  Add Song docstring.
	# TODO:  Add Song str representation.
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
	# TODO:  Add Track docstring.
	# TODO:  Add Track str representation.
	def __init__(self, desc=None):
		self.description = desc
		self.measures = []


	def set_description(self, desc):
		self._description = desc
		return


	def get_description(self):
		return self._description


	description = property(get_description, set_description)


	def append_measure(self, measure=None, **kwargs):
		if measure is None:
			measure = Measure(**kwargs)
		self.measures.append(measure)
		return measure


	def end_track(self):
		end_signal = Event('end_track')
		final_measure = self.append_measure()
		final_beat = final_measure.append_beat()
		final_beat.add_event(end_signal)
		return self



class Measure():
	# TODO:  Add Measure docstring.
	# TODO:  Add Measure str representation.
	def __init__(self, key='C_Maj', time_signature='4/4', add_first_beat=True):
		self.key = key
		self.time_signature = time_signature
		self.complete = False
		self.beats = []
		if add_first_beat:
			self.append_beat()


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


	def set_complete(self, complete):
		self._complete = bool(complete)
		return


	def get_complete(self):
		complete = self._complete
		last_beat = self.beats[-1]
		if not complete and last_beat.complete and self.remaining_duration == 0:
				complete = True
				self.complete = complete
		return complete


	complete = property(get_complete, set_complete)


	def get_remaining_duration(self, beat=None, note=None, method='min'):
		if note == None:
			if beat == None:
				beat = self.beats[-1]
			if beat.notes == []:
				note = Note('C', duration=0)  # make a dummy note with zero duration for calculations
			elif method[:3].lower() == 'min' or method[:5].lower() == 'short':
				note = beat.shortest_note
			elif method[:3].lower() == 'max' or method[:4].lower() == 'long':
				note = beat.longest_note
			else:
				raise AttributeError("Allowed methods for get_remaining_duration are 'min'/'short' and 'max'/'long'")
		elif beat == None:
			for potential_beat in self.beats:
				if note in potential_beat.notes:
					beat = potential_beat
		beat_index = self.beats.index(beat)
		ts = self.time_signature
		total_duration = ts.numerator * Duration(ts.denominator)
		passed_duration = sum([beat.offset for beat in self.beats[:beat_index + 1]])
		passed_duration = passed_duration + note.duration
		remaining_duration = total_duration - passed_duration
		return remaining_duration


	remining_duration = property(get_remaining_duration)


	def append_beat(self, beat=None, offset=None):
		if beat is None:
			if offset is None:
				if self.beats == []:
					offset=0
				else:
					if self.beats[-1].notes == []:
						offset = Duration(base=self.time_signature.denominator, mode='inverse')
					else:
						offset = self.beats[-1].shortest_note.duration
			beat = Beat(offset=offset)
		self.beats.append(beat)
		return beat


	def pad_rests(self):
		# TODO:  This needs an extensive unit test.
		last_beat = self.beats[-1]
		if last_beat.notes == []:
			remaining_durations = [self.get_remaining_duration(beat=last_beat)]
			offset = 0
		else:
			remaining_durations = [
				self.get_remaining_duration(beat=last_beat, note=note)
				for note
				in last_beat.notes
			]
			offset = last_beat.shortest_note.duration

		# remove duplicates from remaining_durations list
		remaining_durations = list(set(remaining_durations))
		remaining_durations.sort(reverse=True)

		# TODO:  Fix this...
		previous_remaining_duration = remaining_durations[0] + offset
		for remaining_duration in remaining_durations:
			beat = self.append_beat(offset=offset)
			# TODO:  This needs to recurse to add multiple beats/notes if Duration isn't expanded.
			beat.add_note(Rest(remaining_duration))
			offset = previous_remaining_duration - remaining_duration
			previous_remaining_duration = remaining_duration

		self.complete = True
		return



class Beat():
	# TODO:  Add Beat docstring.
	# TODO:  Add Beat str representation.
	def __init__(self, offset='quarter'):
		self.offset = offset
		self.notes = []
		self.events = []
		self.complete = False


	def set_offset(self, offset):
		offset = Duration(offset)
		self._offset = offset
		return


	def get_offset(self):
		offset = self._offset
		return offset


	offset = property(get_offset, set_offset)


	def set_complete(self, complete):
		complete = bool(complete)
		self._complete = complete
		return


	def get_complete(self):
		complete = self._complete
		return complete


	complete = property(get_complete, set_complete)
	ended = property(get_complete, set_complete)


	def get_shortest_note(self):
		short_note = min([(note.duration.length, note) for note in self.notes])[1]
		return short_note


	shortest_note = property(get_shortest_note)


	def get_longest_note(self):
		long_note = max([(note.duration.length, note) for note in self.notes])[1]
		return long_note


	longest_note = property(get_longest_note)


	def add_note(self, note):
		self.notes.append(note)
		return note


	def add_event(self, event):
		self.events.append(event)
		return event



class Note(util.CheckArg):
	# TODO:  Add Note docstring.
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
		# TODO:  Add more info to Note string representation.
		repstring = self.name + '_' + str(self.octave)
		return repstring



class Rest():
	# TODO:  Add Rest docstring.
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
	# TODO:  Add Event docstring.
	def __init__(self, name=None, descr=None):
		self.name = name
		self.description = descr



class Duration(util.CheckArg):
	'''
	Duration(duration=None, name=None, length=None, base=None, count=1, mode='inverse', dot=False)

	Create a Duration object.  If no parameters are given, creates an
	uninitialized instance.  Can be (re-)initialized with the set() method with
	the same parameters.  Durations can be compared with other instances of
	Duration and number-based objects.  Durations can be added, subtracted,
	multiplied and divided with other Duration instances and number-based
	objects, returning either a new Duration instance or float number,
	depending on what makes sense with the units and allowed duration lengths.
	It is generally advisable to not set durations longer than a measure and to
	instead set the tie flag for the note or rest to carry over to another
	instance in the next measure.

	Parameters
	----------
	duration : str, float, int power of 2 <= 64, int <= 6, or Duration instance (optional)
		The note or rest generalized duration parameter.  This attempts to
		determine the intended other remaining parameters based on the value
		and type of the argument.  If a string is passed, this is treated as
		the name parameter.  If an integer or float is passed, this is treated
		as the length parameter for values less than one or the base parameter
		for values greater than one.  If an existing Duration object is given,
		setup is skipped and that object is returned.
	name : str (optional)
		Specify the duration name.  Allowed names are English note names
		between 'whole' and 'sixty-fourth', optionally prepended with 'dotted '
		to override and enable the dot option (e.g. 'dotted thirty-second').
		If both base and name are passed when setting the duration, overrides
		base.  Respects the dot parameter unless name begins with 'dotted', in
		which case dot is set to True.
	length : float or int (optional)
		Specify the duration length.  This is the count divided by the duration
		base.  Ambiguous lengths set the count and base to the smallest valid
		values (e.g. length=0.5 sets the duration as one half note instead of
		two quarter notes) unless the count or base parameters are explicitly
		specified.
	base : int power of 2 <= 64 or int <= 6 (optional)
		Specify the duration base.  Allowed values are powers of 2 between 1
		and 64 if mode is 'inverse' (where '1' is a whole note and '64' is a
		sixty-fourth note) or integers between 0 and 6 if mode is
		'inverse_power' (where 0 is a whole note and 6 is a sixty-fourth note).
		The special case of a zero-length duration is created by setting base
		to 'zero' or 0 with mode set to the default 'inverse'.
	count : int (optional)
		Specify how many occurrences of the base comprise the duration length.
	mode : {'inverse', 'inverse_power'} (optional)
		Select between specifying the base as a power of two directly
		('inverse') or the exponent with which to raise 2 ('inverse_power').
		This option is ignored if base is a string.
	dot : bool (optional)
		Specify whether the duration should be dotted.  If True, the base
		duration is multiplied by 1.5 (e.g., a dotted quarter is three
		eighths).
	'''
	def __init__(self, duration=None, name=None, length=None, base=None, count=1, mode='inverse', dot=False):
		# TODO:  Add count property.
		# TODO:  Need to update Duration class to allow initialization with lengths (e.g. setting offsets).
		# TODO:  Decide how to handle triplets.
		self.names = ['whole', 'half', 'quarter', 'eighth', 'sixteenth', 'thirty-second', 'sixty-fourth', 'zero']
		self.bases = [1, 2, 4, 8, 16, 32, 64, 0]
		self.base = None
		self.dot = None
		if (duration is not None) or (name is not None) or (length is not None) or (base is not None):
			self.set(duration, name, length, count, base, mode, dot)


	def set(self, duration=None, name=None, length=None, count=1, base=None, mode='inverse', dot=False):
		if (duration is None) and (name is None) and (length is None) and (base is None):
			raise AttributeError("Setting a Duration requires setting at least one parameter.")
		self.count = count
		self.dot = dot

		if duration is not None:
			if (name is None) and (type(duration) == str):
				name = duration
			elif (length is None) and (duration < 1):
				length = duration
			elif (base is None) and (duration >= 1):
				base = duration

		if name is not None:
			self.name = name
		elif length is not None:
			self.length = length
		elif mode == 'inverse':
			self.base = base
		elif mode == 'inverse_power':
			self.base = 2**base
		else:
			raise AttributeError("Duration class mode options are 'inverse' and 'inverse_power'.")
		return self


	def set_name(self, name):
		if type(name) is not str:
			raise AttributeError("Duration class 'name' attribute must be a string.")
		if name[:6].lower() == 'dotted':
			self.dot = True
			name = name[7:]
		if name.lower() in self.names:
			list_index = self.names.index(name.lower())
			self.base = self.bases[list_index]
		else:
			raise AttributeError("Valid Duration names:  %s" % str(self.names))
		return


	def get_name(self):
		list_index = self.bases.index(self.base)
		basename = self.names[list_index]
		if self.dot:
			name = 'dotted ' + basename
		else:
			name = basename
		return name


	name = property(get_name, set_name)


	def set_base(self, base):
		if (base not in self.bases) and (base is not None):
			raise AttributeError(f"Attempted to set base {base}.  Duration base must be a power of 2 between 1 and 64.")
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


	def set_length(self, length):
		print('Warning:  Duration lengths are set via the base and dot attributes...skipping.')
		return


	def get_length(self):
		if self.base == 0:
			length = 0
		else:
			length = 1. / self.base
		if self.dot:
			length = length * 1.5
		return length


	length = property(get_length, set_length)


	# TODO:  Update Duration operators to be better at returning Duration instances.
	def __add__(self, other):
		if isinstance(other, self.__class__):
			result = self.length + other.length
		else:
			result = self.length + other
		return result


	def __radd__(self, other):
		return self.__add__(other)


	def __sub__(self, other):
		if isinstance(other, self.__class__):
			result = self.length - other.length
		else:
			result = self.length - other
		return result


	def __rsub__(self, other):
		if isinstance(other, self.__class__):
			result = other.length - self.length
		else:
			result = other - self.length
		return result


	def __mul__(self, other):
		if isinstance(other, self.__class__):
			result = self.length * other.length
		else:
			try:
				result = Duration(self.base / other, dot=self.dot)
			except AttributeError:
				result = self.length * other
		return result


	def __rmul__(self, other):
		return self.__mul__(other)


	def __truediv__(self, other):
		if isinstance(other, self.__class__):
			result = self.length / other.length
		else:
			try:
				result = Duration(self.base * other, dot=self.dot)
			except AttributeError:
				result = self.length / other
		return result


	def __rtruediv__(self, other):
		if isinstance(other, self.__class__):
			result = other.length / self.length
		else:
			result = other / self.length
		return result


	def __eq__(self, other):
		if isinstance(other, self.__class__):
			result = (self.base == other.base) and (self.dot == other.dot)
		else:
			result = self.length == other
		return result


	def __gt__(self, other):
		if isinstance(other, self.__class__):
			result = self.length > other.length
		else:
			result = self.length > other
		return result


	def __ge__(self, other):
		if isinstance(other, self.__class__):
			result = self.length >= other.length
		else:
			result = self.length >= other
		return result


	def __lt__(self, other):
		if isinstance(other, self.__class__):
			result = self.length < other.length
		else:
			result = self.length < other
		return result


	def __le__(self, other):
		if isinstance(other, self.__class__):
			result = self.length <= other.length
		else:
			result = self.length <= other
		return result


	def __str__(self):
		return self.name



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
		# TODO:  Move Key __str__ functionality to name property.
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
		# TODO:  Move TimeSig __str__ functionality to name property.
		numer = self.numerator
		denom = self.denominator
		if (numer is not None) and (denom is not None):
			repstring = str(numer) + '/' + str(denom)
		else:
			repstring = 'Uninitialized time signature'
		return repstring



if __name__ == "__main__":
	main()

