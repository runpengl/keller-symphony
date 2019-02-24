# -*- coding: utf-8 -*-
import numpy as np
import wave, pyaudio
from piano import *
from constants import *

tones = np.array([get_fr_hz(i+1) for i in range(88)])

def match_tone(f):
	if f == 0:
		return None
	match = np.argmin(abs(tones-f)) + 1
	return match

def extract_tone(filename, play=False):
	print "Processing... " + filename
	chunk = 4096
	try:
		wf = wave.open(filename)
	except:
		return None
	swidth = wf.getsampwidth()
	RATE = wf.getframerate()
	duration = wf.getnframes() / float(RATE)
	# use a Blackman window
	window = np.blackman(chunk)
	# open stream
	if play:
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(swidth),
	                channels = wf.getnchannels(),
	                rate = RATE,
	                output = True)

	# read some data
	data = wf.readframes(chunk)
	# play stream and find the frequency of each chunk
	fr = 0
	while len(data) == chunk*swidth:
	    # write data out to the audio stream
	    if play:
	    	stream.write(data)
	    # unpack the data and times by the hamming window
	    indata = np.array(wave.struct.unpack("%dh" % (len(data)/swidth), data))*window
	    # Take the fft and square each value
	    fftData = abs(np.fft.rfft(indata))**2
	    # find the maximum
	    which = fftData[1:].argmax() + 1
	    # use quadratic interpolation around the max
	    if which != len(fftData)-1:
	        y0,y1,y2 = np.log(fftData[which-1:which+2:])
	        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
	        # find the frequency and output it
	        fr = (which + x1) * RATE / chunk
	    else:
	        fr = which * RATE / chunk
	    data = wf.readframes(chunk)
	tone = match_tone(fr)
	print "Key #: " + str(tone)
	if play:
		if data:
			stream.write(data)
		stream.close()
		p.terminate()
	return tone

def pad(s, n):
	s = str(s)
	while len(s) < n:
		s = "0" + s
	return s

ascii_notes = ""
for i in range(6*len(BRAILLE_CLUEPHRASE.replace(" ", ""))):
	tone = extract_tone("files/{0}.wav".format(pad(i+1, 3)))
	if tone is not None:
		ascii_notes += chr(tone)
		print ascii_notes

print ascii_notes
assert ascii_notes == "".join(map(chr, INTERSPERSED_NOTES))