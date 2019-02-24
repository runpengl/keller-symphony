notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

KEYS = []
NUM_KEYS = 88

for i in range(1, NUM_KEYS + 1):
	octave = (i + 8) // 12
	note = (i + 8) % 12
	eng_notation = notes[note] + str(octave)
	KEYS.append(eng_notation)

def get_nth_key(eng_notation):
	return KEYS.index(eng_notation) + 1

def get_fr_hz(nth_key):
	return 440. * 2 ** ((nth_key-49)/12.)