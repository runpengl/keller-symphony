import pysynth as ps
from piano import *
import os

os.system("rm pure_tones/*.wav")

for (i, k) in enumerate(KEYS):
	ps.make_wav([(k.lower() + "*", 4)], fn="pure_tones/{}.wav".format(i+1), boost=0.001)