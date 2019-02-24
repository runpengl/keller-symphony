import pysynth_b as ps_piano
import pysynth as ps
from piano import *

for (i, k) in enumerate(KEYS):
	ps.make_wav([(k.lower(), 4)], fn="pure_tones/{}.wav".format(i+1))
	ps_piano.make_wav([(k.lower(), 4)], fn="piano_tones/{}.wav".format(i+1))