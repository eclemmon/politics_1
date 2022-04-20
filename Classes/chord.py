from Classes.note import Note


class Chord:
    """
    Chord class for operating on sets of notes.
    Note: Some duplicating logic with Scale class. In the future, create an abstracted note collection class and
    subclass Chord and Scale from there.
    """
    def __init__(self, *notes: Note):
        """
        Initialization for Chord Class
        :param notes: tuple of Notes
        """
        for i in notes:
            assert isinstance(i, Note)
        self.notes = notes

    def __str__(self):
        """
        Prints chord prettily based on the note's midi note number
        :return: str
        """
        result = '| '
        for index, note in enumerate(self.notes):
            if index == len(self.notes)-1:
                result += str(note).split()[0]
            else:
                result += str(note).split()[0] + ", "
        result += ' | or | '
        for note in self.notes:
            result += str(note.midi_note_number) + ' '
        result += '|'
        return result

    def __repr__(self):
        """
        Representation of a chord
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def __eq__(self, other):
        """
        Tests numerical equivalence of the midi note numbers in all notes. Useful for testing whether
        two chords are the same chord (including the octave placement) But not the same object.
        :param other: Chord
        :return: Boolean
        """
        if not isinstance(other, Chord):
            return NotImplemented

        return self.notes == other.notes

    def __hash__(self):
        """
        Hash method for testing whether two Chords are the same object (and necessarily have the same Notes).
        :return: int
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def transpose(self, num: int):
        """
        Transposes self's midi note numbers by num octaves.
        :param num: int
        :return: None
        """
        for note in self.notes:
            note.transpose(num)

    def transpose_return_new(self, num: int):
        """
        Creates a new Chord that is transposed by num octaves.
        :param num: int
        :return: Note
        """
        return Chord(*[Note(note.midi_note_number + (num * 12)) for note in self.notes])

    def get_bass_note(self):
        """
        Gets the bass note of the chord
        :return: Note
        """
        return self.notes[0]


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    c7 = Chord(Note(60), Note(64), Note(67), Note(70))
    print(c_major)
    print(c7)
    c7.transpose(4)
    print(c7)
