from note import Note

class Chord:
    def __init__(self, *notes):
        for i in notes:
            assert isinstance(i, Note)
        self.notes = notes

    def __repr__(self):
        result = ''
        for note in self.notes:
            result += " | " + str(note) + " | "
        return result



if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    c7 = Chord(Note(60), Note(64), Note(67), Note(70))
    print(c_major)
    print(c7)
