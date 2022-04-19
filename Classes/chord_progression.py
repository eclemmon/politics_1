from Classes.chord import Chord
from Classes.note import Note


class ChordProgression:
    """
    Chord progression class for storing an iterable of chords.
    """
    def __init__(self, *chords: tuple):
        """
        Initializes ChordProgression class
        :param chords: tuple of Chords
        """
        for chord in chords:
            assert isinstance(chord, Chord), "{} is expected to be a Chord class.".format(chord)
        self.chords = chords

    def __str__(self):
        """
        Prettily prints the array of chords.
        :return: str
        """
        return str([chord for chord in self.chords])

    def __repr__(self):
        """
        Representation of ChordProgression class
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def transpose(self, num: int):
        """
        Transposes the midi note numbers of self's Chords by num octaves.
        :param num: int
        :return: None
        """
        for chord in self.chords:
            chord.transpose(num)

    def transpose_return_new(self, num: int):
        """
        Transposes the midi note numbers of self's Chords by num octaves and instantiates new Chords and a new Chord
        Progression instance.
        :param num: int
        :return: None
        """
        return ChordProgression(tuple([chord.transpose_return_new(num) for chord in self.chords]))


if __name__ == "__main__":
    c_major = Chord(Note(0), Note(4), Note(7))
    CM7 = Chord(Note(0), Note(4), Note(7), Note(11))
    chords = [c_major, CM7]
    simple_harmony = ChordProgression(chords)
    print(simple_harmony)