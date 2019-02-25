# -*- coding: utf-8 -*-

s = '''ASCII Hex,ASCII Glyph,Braille Dots,Braille Meaning
40	@	010000	⠈ 
41	A	100000	⠁ 	a
42	B	101000	⠃ 	b
43	C	110000	⠉ 	c
44	D	110100	⠙ 	d
45	E	100100	⠑ 	e
46	F	111000	⠋ 	f
47	G	111100	⠛ 	g
48	H	101100	⠓ 	h
49	I	011000	⠊ 	i
4A	J	011100	⠚ 	j
4B	K	100010	⠅ 	k
4C	L	101010	⠇ 	l
4D	M	110010	⠍ 	m
4E	N	110110	⠝ 	n
4F	O	100110	⠕ 	o
50	P	111010	⠏ 	p
51	Q	111110	⠟ 	q
52	R	101110	⠗ 	r
53	S	011010	⠎ 	s
54	T	011110	⠞ 	t
55	U	100011	⠥ 	u
56	V	101011	⠧ 	v
57	W	011101	⠺ 	w
58	X	110011	⠭ 	x
59	Y	110111	⠽ 	y
5A	Z	100111	⠵ z'''.split("\n")[1:]

BRAILLE_DICT = {}
BRAILLE_DICT[" "] = { "bin": "000000", "dots": "\t" }

for line in s:
	parts = line.split()
	BRAILLE_DICT[parts[1]] = { "bin": parts[2], "dots": parts[3] }

def decode(inp, form="bin"):
	for k in BRAILLE_DICT:
		if BRAILLE_DICT[k][form] == inp:
			return k
	raise Exception("Could not decode: " + inp)

def encode(letter, form="bin"):
	letter = letter.upper()
	if letter in BRAILLE_DICT:
		return BRAILLE_DICT[letter][form]
	raise Exception("Could not encode: " + letter)

def main():
	print("Letter\tBinary\tDots\n")
	print("\n".join(["\t".join(map(unicode, row)) for row in [[decode(encode(k)), encode(k), encode(k, "dots")] for k in sorted(BRAILLE_DICT.keys())]]))

if __name__ == "__main__":
	main()
