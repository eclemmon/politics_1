from Classes.chord import Chord
from Classes.note import Note


class Harmony:
    def __init__(self, chords):
        for chord in chords:
            assert isinstance(chord, Chord), "{} is expected to be a Chord class.".format(chord)
        self.chords = chords

    def __repr__(self):
        return str([chord for chord in self.chords])

    def transpose(self, num):
        self.chords = [chord.transpose(num) for chord in self.chords]


if __name__ == "__main__":
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    chords = [c_major, CM7]
    simple_harmony = Harmony(chords)
    print(simple_harmony)