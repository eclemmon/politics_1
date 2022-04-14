from Classes.note import Note


class Scale:
    def __init__(self, *notes):
        for i in notes:
            assert isinstance(i, Note) or isinstance(i, tuple)
        self.notes = notes

    def __eq__(self, other):
        if not isinstance(other, Scale):
            return NotImplemented

        return self.notes == other.notes

    def __len__(self):
        return len(self.notes)

    def transpose(self, num):
        for note in self.notes:
            note.transpose(num)

    def modal_transpose(self, scale_degree):
        self.notes = tuple(self.notes[scale_degree:] + self.notes[:scale_degree])

    def modal_transpose_return_new(self, scale_degree):
        return Scale(tuple(self.notes[scale_degree:] + self.notes[:scale_degree]))

    def transpose_return_new(self, num):
        return Scale(tuple([Note(note.midi_note_number + num) for note in self.notes]))
