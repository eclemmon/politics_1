class Note:
    def __init__(self, midi_note_number):
        self.midi_note_number = midi_note_number

    def __repr__(self):
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

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented

        return self.midi_note_number == other.midi_note_number

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __add__(self, other):
        if isinstance(other, Note):
            return Note(self.midi_note_number + other.midi_note_number)
        elif isinstance(other, int):
            return Note(self.midi_note_number + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Note):
            return Note(self.midi_note_number - other.midi_note_number)
        elif isinstance(other, int):
            return Note(self.midi_note_number - other)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Note):
            return self.midi_note_number < other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number < other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Note):
            return self.midi_note_number <= other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number <= other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Note):
            return self.midi_note_number > other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number > other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Note):
            return self.midi_note_number >= other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number >= other
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Note):
            return self.midi_note_number != other.midi_note_number
        elif isinstance(other, int):
            return self.midi_note_number != other
        else:
            return NotImplemented

    def transpose(self, num):
        self.midi_note_number = self.midi_note_number + (num * 12)

    def transpose_return_new(self, num):
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

