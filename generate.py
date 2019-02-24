import sys, os
import config as puzzle_config
import braille
from shutil import copyfile

OUTPUT_HTML = "puzzle.html"
HTML_TEMPLATE = "template/puzzle_template.html"

os.system("rm files/*.wav")

copyfile(HTML_TEMPLATE, OUTPUT_HTML)

def to_html_table(file_grid):
	out = "<table>\n"

	for (i, row) in enumerate(file_grid):
		out += "<tr>\n"
		out += "".join(map(lambda x: "<td><a href='{0}' target='_blank'>&#119136;</a></td>".format(x), row))
		out += "\n</tr>"
		if (i < len(file_grid) - 1):
			out += "\n"

	out += "\n</table>"
	return out

def pad(s, n):
	s = str(s)
	while len(s) < n:
		s = "0" + s
	return s

NOTES_INDEX = 0

def get_audio_files(braille_codes, start_index):
	global NOTES_INDEX

	braille_codes = [tuple(x) for x in braille_codes]
	n = len(braille_codes)
	dot_grid = [["0","0"]*n for i in range(3)]

	for (i, code) in enumerate(braille_codes):
		'''(p1, p2, p3, p4, p5, p6) = code
		dot_grid[0][i*2]   = p1
		dot_grid[0][i*2+1] = p2
		dot_grid[1][i*2]   = p3
		dot_grid[1][i*2+1] = p4
		dot_grid[2][i*2]   = p5
		dot_grid[2][i*2+1] = p6

		if i == len(braille_codes)-1:
			print "\n".join(map(lambda x:"".join(x), dot_grid))'''

		for (j, p) in enumerate(code):
			filename = "files/{}.wav".format(pad(start_index, 3))
			if p == "1":
				# tone file
				copyfile("pure_tones/{0}.wav".format(puzzle_config.INTERSPERSED_NOTES[NOTES_INDEX]), filename)
				NOTES_INDEX += 1
			else:
				# silent file
				copyfile("pure_tones/silent.wav", filename)
			
			dot_grid[j//2][i*2+j%2] = filename
			start_index += 1

	return dot_grid

def main():
	audio_index = 1
	BRAILLE_CLUE_WORDS = puzzle_config.BRAILLE_CLUEPHRASE.split(" ")
	for (i, word) in enumerate(BRAILLE_CLUE_WORDS):
		audio_files = get_audio_files(map(lambda x:braille.BRAILLE_DICT[x]["bin"], word), audio_index)
		audio_index += len(word) * 6
		html_string = to_html_table(audio_files)

		contents = ""
		with open(OUTPUT_HTML, "r") as f:
			contents = f.read()
			f.close()

		last_write = (i == len(BRAILLE_CLUE_WORDS) - 1)

		with open(OUTPUT_HTML, "w") as f:
			new_contents = contents.replace(">>content", html_string + "<br/>\n" + (">>content" if not last_write else ""))
			f.write(new_contents)
			f.close()

	assert NOTES_INDEX == len(puzzle_config.INTERSPERSED_NOTES)
	assert audio_index-1 == 6 * len("".join(BRAILLE_CLUE_WORDS))

if __name__ == "__main__":
	main()