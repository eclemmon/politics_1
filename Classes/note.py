class Note:
    """
    A simple note class with logic for printing self, object equivalence and comparison. Also logic for transposition.
    """
    def __init__(self, midi_note_number: int):
        """
        Initialization for Note class
        :param midi_note_number: int
        """
        self.midi_note_number = midi_note_number

    def __str__(self):
        """
        Prints notes prettily based on the midi note number
        :return: str
        """
        NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = self.midi_note_number // 12 - 1
        note_index = self.midi_note_number % 12
        pretty_midi = "{flat}-{octave} or {sharp}-{octave}".format(
            flat=NOTES_FLAT[note_index],
            octave=octave,
            sharp=NOTES_SHARP[note_index]
        )
        return pretty_midi

    def __repr__(self):
        """
        Representation of a note.
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def __eq__(self, other):
        """
        Tests numerical equivalence of the midi note numbers. Useful for testing whether two notes are the same
        note. But not the same object.
        :param other: Note
        :return: Boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number == other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number == other
        else:
            return NotImplemented

    def __hash__(self):
        """
        Hash method for testing whether two notes are the object (and necessarily have the same note number).
        :return: int
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def __add__(self, other):
        """
        Creates a new note object by adding self.midi_note_number to other. Can add another Note object or an integer.
        :param other: Note || int
        :return: Note
        """
        if isinstance(other, Note):
            return Note(self.midi_note_number + other.midi_note_number)
        elif isinstance(other, int):
            return Note(self.midi_note_number + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Creates a new note object by subtracting self.midi_note_numberfrom other. Can add another Note object
        or an integer.
        :param other: Note || int
        :return: Note
        """
        if isinstance(other, Note):
            return Note(self.midi_note_number - other.midi_note_number)
        elif isinstance(other, int):
            return Note(self.midi_note_number - other)
        else:
            return NotImplemented

    def __lt__(self, other):
        """
        Less than comparison of midi note numbers or self.midi_note_number to another integer.
        :param other: Note || int
        :return: boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number < other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number < other
        else:
            return NotImplemented

    def __le__(self, other):
        """
        Less than or equal to comparison of midi note numbers or self.midi_note_number to another integer.
        :param other: Note || int
        :return: boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number <= other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number <= other
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        Greater than comparison of midi note numbers or self.midi_note_number to another integer.
        :param other: Note || int
        :return: boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number > other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number > other
        else:
            return NotImplemented

    def __ge__(self, other):
        """
        Greater than or equal to comparison of midi note numbers or self.midi_note_number to another integer.
        :param other: Note || int
        :return: boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number >= other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number >= other
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        Not equal to comparison of midi note numbers or self.midi_note_number to another integer.
        :param other: Note || int
        :return: boolean
        """
        if isinstance(other, Note):
            return self.midi_note_number != other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number != other
        else:
            return NotImplemented

    def transpose(self, num):
        """
        Transposes self's midi note number by num octaves.
        :param num: int
        :return: None
        """
        self.midi_note_number = self.midi_note_number + (num * 12)

    def transpose_return_new(self, num):
        """
        Creates a new note that is transposed by num octaves.
        :param num: int
        :return: Note
        """
        return Note(self.midi_note_number + (num * 12))


if __name__ == '__main__':
    c = Note(72)
    db = Note(73)
    print(c)
    print(db)
    db.transpose(-2)
    print(db.midi_note_number)
    print(db)
    print(db+7)

