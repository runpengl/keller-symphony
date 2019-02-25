from __future__ import print_function

import numpy as np
import wave, pyaudio
import piano as piano
import braille as braille
import config as puzzle_config

TONES = np.array([piano.get_fr_hz(n_key+1) for n_key in range(88)])

def match_tone(f_Hz):
	try:
		int(f_Hz)
	except:
		return None
	if f_Hz == 0:
		return None
	match = np.argmin(abs(TONES - f_Hz)) + 1 # nth piano key
	return match

def extract_tone(filename, play=False):
	print("\nProcessing... %s" % filename)
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
			try:
				y0, y1, y2 = np.log(fftData[which-1:which+2:])
				x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
				# find the frequency and output it
				fr = (which + x1) * RATE / chunk
			except:
				pass
		else:
			fr = which * RATE / chunk
		data = wf.readframes(chunk)
	tone = match_tone(fr)
	if tone is not None:
		print("Keyboard #: %s" % tone)
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

def main():
	ascii_notes = ""
	braille_dots = ""
	braille_decode = ""
	CLUE_LETTERS = puzzle_config.BRAILLE_CLUEPHRASE.replace(" ", "")
	for i in range(6*len(CLUE_LETTERS)):
		tone = extract_tone("files/{0}.wav".format(pad(i+1, 3)))
		if tone is not None:
			braille_dots += "1"
			ascii_notes += chr(tone)
		else:
			braille_dots += "0"
		if len(braille_dots) == 6:
			braille_decode += braille.decode(braille_dots)
			braille_dots = ""

	print("\n=== Braille:\n%s " % braille_decode)

	print("\n=== Extraction:\n%s " % ascii_notes)
	assert ascii_notes == "".join(map(chr, puzzle_config.INTERSPERSED_NOTES))

	bad_notes = ascii_notes.split(": ")[1].split(" ")[0]
	bad_notes = [ord(x) for x in bad_notes]
	print("\n=== Bad notes:\n%s " % bad_notes)

	extract_answer = "".join([chr(x - puzzle_config.CLUED_MELODY[i] + 64) for (i, x) in enumerate(bad_notes)])
	assert extract_answer == puzzle_config.FINAL_SOLUTION
	print("\n=== Answer:\n%s " % extract_answer)

if __name__ == "__main__":
	main()