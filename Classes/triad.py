from Classes.chord import Chord
from Classes.note import Note


class Triad(Chord):
    """
    Triad class. SubClass of a chord with only three notes.
    """
    def __init__(self, note_1: Note, note_2: Note, note_3: Note):
        """
        Initialization for Triad
        :param note_1: Note
        :param note_2: Note
        :param note_3: Note
        """
        self.notes = note_1, note_2, note_3


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    print(c_major)
