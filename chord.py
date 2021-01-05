from note import Note


class Chord:
    def __init__(self, *notes):
        for i in notes:
            assert isinstance(i, Note)
        self.notes = notes

    def __repr__(self):
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

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return NotImplemented

        return self.notes == other.notes

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def transpose(self, num):
        self.notes = [note.transpose(num) for note in self.notes]


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    c7 = Chord(Note(60), Note(64), Note(67), Note(70))
    print(c_major)
    print(c7)
