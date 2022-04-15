from Classes.chord import Chord
from Classes.note import Note


class ChordProgression:
    def __init__(self, chords):
        for chord in chords:
            assert isinstance(chord, Chord), "{} is expected to be a Chord class.".format(chord)
        self.chords = chords

    def __repr__(self):
        return str([chord for chord in self.chords])

    def transpose(self, num):
        for chord in self.chords:
            chord.transpose(num)

    def transpose(self, num):
        for note in self.notes:
            note.transpose(num)

    def transpose_return_new(self, num):
        return ChordProgression([chord.transpose_return_new(num) for chord in self.chords])


if __name__ == "__main__":
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    chords = [c_major, CM7]
    simple_harmony = ChordProgression(chords)
    print(simple_harmony)