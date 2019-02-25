from __future__ import print_function
import piano
import braille

BRAILLE_CLUEPHRASE = "NICE JOB NOW DECODE NONSILENT TONES AS ASCII USING EIGHTY EIGHT KEY PIANO KEYBOARD"

# cannot contain Y or Z
NOTES_CLUEPHRASE = "SHIFT DOWN THESE 47 NOTES TO MAKE THE FAMOUS TUNE FROM DEAF COMPOSER'S 9TH SIMPHONI: <>"\
+ " BEGIN ON MID-C4, GO 12 MEASURES. USE SHIFT AMOUNTS TO GET SOLUTION"

# ensure in piano key range
for c in NOTES_CLUEPHRASE:
	assert ord(c) <= 88

# "Ode to Joy" in key of C
CLUED_MELODY = ["B3", "B3", "C4", "D4", "D4", "C4", "B3", "A3", "G3", "G3", "A3", "B3", "B3", "A3", "A3"] \
+ ["B3", "B3", "C4", "D4", "D4", "C4", "B3", "A3", "G3", "G3", "A3", "B3", "A3", "G3", "G3"] \
+ ["A3", "A3", "B3", "G3", "A3", "B3", "C4", "B3", "G3", "A3", "B3", "C4", "B3", "A3", "G3", "A3", "D3"]

CLUED_MELODY_NOTE_LEN = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2.67, 8, 2] \
+ [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2.67, 8, 2] \
+ [4, 4, 4, 4, 4, 8, 8, 4, 4, 4, 8, 8, 4, 4, 4, 4, 4]

# "Ode to Joy" starting on Middle C
CLUED_MELODY = [x + piano.get_nth_key("C4") - piano.get_nth_key(CLUED_MELODY[0]) \
for x in map(piano.get_nth_key, CLUED_MELODY)]
#print "\nMelody: {0}".format(map(piano.get_eng_notation, CLUED_MELODY))
FINAL_SOLUTION = "THE ANSWER IS XXXX LYRIC WORD THAT IS SUNG ON MARKED NOTES".replace(" ", "")

assert len(FINAL_SOLUTION) <= len(CLUED_MELODY)

SOLUTION_SHIFT = [CLUED_MELODY[i] + (ord(c) - ord("A") + 1) for (i, c) in enumerate(FINAL_SOLUTION)]
#print "\nBad notes: {0}".format(map(piano.get_eng_notation, SOLUTION_SHIFT))

NOTES_CLUEPHRASE = NOTES_CLUEPHRASE.replace("<>", "".join(map(chr, SOLUTION_SHIFT)))

'''interperse_interval = len(NOTES_CLUEPHRASE) // len(SOLUTION_SHIFT)
INTERSPERSED_NOTES = []
for (i, c) in enumerate(SOLUTION_SHIFT):
	start, end = i*interperse_interval, (i+1)*interperse_interval
	INTERSPERSED_NOTES += (map(ord, NOTES_CLUEPHRASE)[start:end] + [c])
INTERSPERSED_NOTES += map(ord, NOTES_CLUEPHRASE)[len(SOLUTION_SHIFT)*interperse_interval:]'''

INTERSPERSED_NOTES = [ord(x) for x in NOTES_CLUEPHRASE]

melody_begin_index = NOTES_CLUEPHRASE.index(": ") + 2
melody_end_index = NOTES_CLUEPHRASE.index(" BEGIN")

assert len(SOLUTION_SHIFT) == melody_end_index - melody_begin_index

INTERSPERSED_NOTES_LEN = [4] * melody_begin_index \
+ CLUED_MELODY_NOTE_LEN[0:melody_end_index-melody_begin_index] \
+ [4] * (len(INTERSPERSED_NOTES) - melody_end_index)

assert len(INTERSPERSED_NOTES_LEN) == len(INTERSPERSED_NOTES)

#assert len(INTERSPERSED_NOTES) == len(NOTES_CLUEPHRASE) + len(FINAL_SOLUTION)

n_braille_dots = "".join(map(braille.encode, BRAILLE_CLUEPHRASE)).count("1")
assert n_braille_dots == len(INTERSPERSED_NOTES)

if __name__ == "__main__":
	# sanity check
	print(n_braille_dots, len(INTERSPERSED_NOTES))
	print("\nKeyboard #'s:\n%s" % INTERSPERSED_NOTES)
	print("\nASCII decode:\n%s" % "".join(map(chr, INTERSPERSED_NOTES)))
