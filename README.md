# Für Helen
 
Generates deaf audio files and positions them in 3x2 Braille grid to create puzzle with a desired puzzle-hunt answer.
Because [Beethoven is simply awesome](http://stringsmagazine.com/helen-kellers-stunning-description-of-hearing-beethovens-ninth-symphony/).

## Config

`python -m pip install pysynth pyaudio`

Modify clue phrases and desired solution in `contants.py`

Run `python generate.py` to output puzzle into HTML file. Add styling/flavor-text as necessary.

## Solve

1. Interpret the non-silent tones as Braille dots => get instruction to decode piano keys as ASCII.
2. Apply DFT to auto-detect pitches => map each pitch to Nth piano key (https://en.wikipedia.org/wiki/Piano_key_frequencies)
3. Decode piano keys as ASCII (e.g. High C#6 = key #65 => ascii "A") to reveal clue phrase:
   **"Shift down extra notes to create tune from deaf composer's 9th symphony, starting on middle C. Then decode shifts as letters"**

4. Final extraction

```python 
# Extra Notes
['G#4', 'F4', 'G5', 'G#4', 'C5', 'G#5', 'C#4', 'E4', 'F4', 'A#4', 'B3', 'C5', 'G5', 'C#5', 'A#4', 'A5', 'G#5', 'A#4', 'F#5', 'F5', 'E4', 'C5', 'G5', 'C#4', 'C5', 'F#4', 'F#5', 'B3', 'D#5', 'C#4']

# "Ode to Joy" starting on Middle C
['C4', 'C4', 'C#4', 'D#4', 'D#4', 'C#4', 'C4', 'A#3', 'G#3', 'G#3', 'A#3', 'C4', 'C4', 'A#3', 'A#3', 'C4', 'C4', 'C#4', 'D#4', 'D#4', 'C#4', 'C4', 'A#3', 'G#3', 'G#3', 'A#3', 'C4', 'A#3', 'G#3', 'G#3']

# Number of keys to shift
[8, 5, 18, 5, 9, 19, 1, 6, 9, 14, 1, 12, 19, 15, 12, 21, 20, 9, 15, 14, 3, 12, 21, 5, 16, 8, 18, 1, 19, 5]
=> "HERE IS A FINAL SOLUTION CLUEPHRASE"
```
