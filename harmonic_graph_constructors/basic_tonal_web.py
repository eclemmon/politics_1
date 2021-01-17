from harmonic_web import HarmonicWeb
from chord import Chord
from note import Note
from Data_Structures import basic_tonal_web_structure

class BasicTonalWeb(HarmonicWeb):
    def __init__(self, starting_chord=None):
        if starting_chord is None:
            midinote_numbers = [0, 4, 7]
        else:
            midinote_numbers = [note.midi_note_number for note in starting_chord.notes]

        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord

        # initializes the riemannian web map and constructs it with the helper function.
        self.web = {}

        # Initializes dict for when search paths are called
        self.breadth_first_path = {}

    def build_web(self, chord=None):
        if chord is None:
            chord = self.starting_chord

        for key, value in basic_tonal_web_structure.basic_major_tonal_web.items():
            new_key = self.build_chord(key)
            new_values = [self.build_chord(next_chord) for next_chord in value]
            self.web[new_key] = new_values


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    basic_af_web = BasicTonalWeb()
    basic_af_web.build_web()
    print(basic_af_web.random_walk_only_new(5))