from chord import Chord
from note import Note

class Triad(Chord):
    def __init__(self, note_1, note_2, note_3):
        self.notes = [note_1, note_2, note_3]

if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    print(c_major)
