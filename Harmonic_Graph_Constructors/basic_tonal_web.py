from harmonic_web import HarmonicWeb
from Classes.chord import Chord
from Classes.note import Note
from Data_Dumps import basic_tonal_web_structure


class BasicTonalWeb(HarmonicWeb):
    """
    BasicTonalWeb class. This class imports data from Data_Dumps.basic_tonal_web_structure to make a graph out of
    the dictionary. Starts in C-major if no starting chord is given. Otherwise, transposes the graph to the starting
    chord as best as possible.
    """
    def __init__(self, starting_chord=None):
        """
        Initialization for BasicTonalWeb class.
        :param starting_chord: None || Chord
        """
        if starting_chord is None:
            midinote_numbers = [0, 4, 7]
        else:
            midinote_numbers = [note.midi_note_number for note in starting_chord.notes]

        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord

        # initializes the basic tonal graph and constructs it with the helper function.
        self.web = {}
        self.build_web()

        # Initializes dict for when search paths are called
        self.breadth_first_path = {}

    def build_web(self):
        """
        Builds the graph from the data.
        :return: None
        """
        diff = self.starting_chord.notes[0].midi_note_number

        for key, value in basic_tonal_web_structure.basic_major_tonal_web.items():
            new_key = self.build_chord([(note+diff) % 12 for note in key])
            new_values = [self.build_chord([(note+diff) % 12 for note in next_chord]) for next_chord in value]
            self.web[new_key] = new_values


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    e_major = Chord(Note(4), Note(8), Note(11))
    basic_af_web = BasicTonalWeb(e_major)
    print(basic_af_web.random_walk_only_new(5))