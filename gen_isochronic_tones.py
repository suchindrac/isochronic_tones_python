#!/usr/bin/env python
# encoding: utf-8
 
"""
Small program for creating Isochronic Tones of desired base frequency, beat frequency and ramp frequencies
"""
 
import math
import wave
import struct
import array
import sys

def make_isochronic_wave(beat_freq, beat_ramp_percent, beat_sampl_rate, beat_time, base_freq, amplitude):

	#
	# The time for which the trapezoidal beat frequency wave is present in the entire cycle
	#
	up_time = 1 / beat_freq
	
	#
	# Gap between consequtive trapezoidal beats
	#
	gap_percent = up_time * 0.15
	
	#
	# To accomodate gaps
	#
	up_time = up_time * 0.85
	
	#
	# Total number of samples
	#
	data_size = beat_sampl_rate * beat_time
	
	#
	# No. of gaps per sec = No. of beats per sec
	#
	no_of_gaps = beat_freq
	
	#
	# Samples per gap = percentage of total time allocated for gaps * No. of samples per sec
	#
	sampls_per_gap = gap_percent * beat_sampl_rate
	
	#
	# Total number of samples in all the gaps
	#
	gap_sampls = no_of_gaps * sampls_per_gap
	
	#
	# Change the beat sample rate to accomodate gaps
	#
	beat_sampl_rate = beat_sampl_rate - gap_sampls
	
	#
	# nsps = Number of Samples Per Second
	#
	# NOTE: Please see the image at: 
	#
	beat_nsps_defined = beat_sampl_rate * up_time

	beat_nsps_inc = beat_nsps_defined * beat_ramp_percent
	
	beat_nsps_dec = beat_nsps_defined * beat_ramp_percent
	
	beat_nsps_stable = beat_nsps_defined - (beat_nsps_inc + beat_nsps_dec)
	
	beat_nsps_undefined = beat_sampl_rate - beat_nsps_defined
	
	#
	# Trapezoidal values
	#
	values = []
	
	#
	# Trapezoidal * sine == Isochronic values
	#
	isoch_values = []
	
	#
	# Samples constructed
	#
	sampls_const = 0

	#
	# Iterate till all the samples in data_size are constructed
	#
	while sampls_const < data_size:
		prev_sampl_value_inc = 0.0
		prev_sampl_value_dec = 1.0
		#
		# Construct one trapezoidal beat wave (remember this is not the entire sample)
		#
		for sampl_itr in range(0, int(beat_sampl_rate)):
			if sampl_itr < beat_nsps_inc:
				value = prev_sampl_value_inc + (1 / beat_nsps_inc)
				prev_sampl_value_inc = value
				values.append(value)
			if sampl_itr > beat_nsps_inc:
				if sampl_itr < (beat_nsps_inc + beat_nsps_stable):
					value = 1
					values.append(value)
				elif (sampl_itr > (beat_nsps_inc + beat_nsps_stable)) and (sampl_itr < (beat_nsps_inc + beat_nsps_stable + beat_nsps_dec)):
					value = prev_sampl_value_dec - (1 / beat_nsps_dec)
					prev_sampl_value_dec = value
					values.append(value)
		
		#
		# Add the gap cycles
		#
		for gap_iter in range(0, int(sampls_per_gap)):
			values.append(0)
		
		#
		# Increment the number of samples constructed to reflect the values
		#
		sampls_const = sampls_const + beat_nsps_defined + gap_sampls

	#
	# Open the wave file
	#
	wav_file = wave.open("beat_wave_%s_%s.wav" % (base_freq, beat_freq), "w")
	
	#
	# Define parameters
	#
	nchannels = 2
	sampwidth = 2
	framerate = beat_sampl_rate
	nframes = data_size
	comptype = "NONE"
	compname = "not compressed"

	wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
	
	#
	# Calculate isochronic wave point values
	#
	value_iter = 0
	
	for value in values:
		isoch_value = value * math.sin(2 * math.pi * base_freq * (value_iter / beat_sampl_rate))
		value_iter = value_iter + 1
		isoch_values.append(isoch_value)

	#
	# Create the wave file (in .wav format)
	#
	for value in isoch_values:
		data = array.array('h')
		data.append(int(value * amplitude / 2)) # left channel
		data.append(int(value * amplitude / 2)) # right channel
	        
		wav_file.writeframes(data.tostring())
	

	wav_file.close()
    
try:
	base_freq = float(sys.argv[1])
	beat_freq = float(sys.argv[2])
	sample_rate = int(sys.argv[3], 10)
	output_time = int(sys.argv[4], 10)
	ramp_percent = float(sys.argv[5])
	amplitude = float(sys.argv[6])
		
	make_isochronic_wave(beat_freq, ramp_percent, sample_rate, output_time, base_freq, amplitude)
except:
	msg = """
program> <base freqency> <beat frequency> <sample rate> <output time> <ramp percent> <amplitude>
"""
	print (msg)

