import pysynth as ps
import piano as piano
import os, sys
import random

def make_tone(nth_key, filename, l=4):
	k = piano.get_eng_notation(nth_key)
	print(k, filename, l)
	return ps.make_wav([(k.lower() + "*", l)], fn=filename, boost=1.*random.randint(100,150) / 100000., bpm=100.)

if __name__ == "__main__":
	try:
		path = sys.argv[1]
	except:
		print("Please specify path for genearted tones")
		exit(1)

	try:
		os.system("mkdir {0}".format(path))
		os.system("rm {0}/*.wav".format(path))
	except:
		pass

	for (i, k) in enumerate(piano.KEYS):
		ps.make_wav([(k.lower() + "*", 4)], fn="{0}/{1}.wav".format(path, i+1), boost=0.001, bpm=100.)

	ps.make_wav([("c4*", 4)], fn="{0}/silent.wav".format(path), boost=0.0, bpm=100.)