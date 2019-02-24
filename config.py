from piano import *
from braille import *

BRAILLE_CLUEPHRASE = "EXCELLENT WORK NOW DECODE THESE TONES AS ASCII USING PIANO KEYBOARD"

# cannot contain Y or Z
NOTES_CLUEPHRASE =   "SHIFT DOWN EACH BAD NOTE TO CREATE A FAMOUS TUNE FROM DEAF COMPOSER'S 9TH SINFONIA. START ON MIDDLE C. USE SHIFT AMOUNTS FOR ANSWER"

# ensure in piano key range
for c in NOTES_CLUEPHRASE:
	assert ord(c) <= 88

# "Ode to Joy" in key of C
CLUED_MELODY = ["B3", "B3", "C4", "D4", "D4", "C4", "B3", "A3", "G3", "G3", "A3", "B3", "B3", "A3", "A3"] + ["B3", "B3", "C4", "D4", "D4", "C4", "B3", "A3", "G3", "G3", "A3", "B3", "A3", "G3", "G3"]

# "Ode to Joy" starting on Middle C
CLUED_MELODY = map(lambda x:x + get_nth_key("C4") - get_nth_key(CLUED_MELODY[0]), map(get_nth_key, CLUED_MELODY))
#print [KEYS[k-1] for k in CLUED_MELODY]
FINAL_SOLUTION = "CONGRATSTHESOLUTIONISXXXXXXXXX"
assert len(FINAL_SOLUTION) <= len(CLUED_MELODY)

SOLUTION_SHIFT = [CLUED_MELODY[i] + (ord(c) - ord("A") + 1) for (i, c) in enumerate(FINAL_SOLUTION)]
#print [KEYS[k-1] for k in SOLUTION_SHIFT]

interperse_interval = len(NOTES_CLUEPHRASE) // len(SOLUTION_SHIFT)

INTERSPERSED_NOTES = []
for (i, c) in enumerate(SOLUTION_SHIFT):
	start, end = i*interperse_interval, (i+1)*interperse_interval
	INTERSPERSED_NOTES += (map(ord, NOTES_CLUEPHRASE)[start:end] + [c])
INTERSPERSED_NOTES += map(ord, NOTES_CLUEPHRASE)[len(SOLUTION_SHIFT)*interperse_interval:]

assert len(INTERSPERSED_NOTES) == len(NOTES_CLUEPHRASE) + len(FINAL_SOLUTION)

n_braille_dots = "".join(map(lambda x:BRAILLE_DICT[x]["bin"], BRAILLE_CLUEPHRASE)).count("1")

#print n_braille_dots, len(INTERSPERSED_NOTES)
assert n_braille_dots == len(INTERSPERSED_NOTES)

if __name__ == "__main__":
	# sanity check
	print INTERSPERSED_NOTES
	print "".join(map(chr, INTERSPERSED_NOTES))