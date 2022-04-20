from Classes.note import Note


class Scale:
    """
    Scale class for containing notes, and additional logic as needed different from the Chord class.
    """
    def __init__(self, *notes: Note):
        """
        Initializtion for Scale class.
        :param notes: tuple of Notes
        """
        for i in notes:
            assert isinstance(i, Note) or isinstance(i, tuple)
        self.notes = notes

    def __str__(self):
        """
        Prints scale prettily based on the note's midi note number
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
        Representation of a scale
        :return: str
        """
        return '<{0}.{1} object at {2} || {3}>'.format(
            type(self).__module__, type(self).__qualname__, hex(id(self)), self.__str__())

    def __eq__(self, other):
        """
        Tests numerical equivalence of the midi note numbers in all notes. Useful for testing whether
        two scales are the same scale (including the octave placement) But not the same object.
        :param other: Chord
        :return: Boolean
        """
        if not isinstance(other, Scale):
            return NotImplemented

        return self.notes == other.notes

    def __len__(self):
        """
        Gets the length of the scale
        :return: int
        """
        return len(self.notes)

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
        return Scale(tuple([Note(note.midi_note_number + num) for note in self.notes]))

    def modal_transpose(self, scale_degree: int):
        """
        Transposes self's midi note numbers by rotating indexes to create a new mode. so self.modal_transpose(1)
        called on a C Major scale will give D dorian.
        :param scale_degree: int
        :return: None
        """
        # TODO transpose rotated notes up and octave.
        self.notes = tuple(self.notes[scale_degree:] + self.notes[:scale_degree])

    def modal_transpose_return_new(self, scale_degree: int):
        """
        Transposes self's midi note numbers by rotating indexes to create and return a new mode and. So
        self.modal_transpose(1) called on a C Major scale will give D dorian.
        :param scale_degree: int
        :return: Scale
        """
        return Scale(tuple(self.notes[scale_degree:] + self.notes[:scale_degree]))


