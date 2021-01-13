from chord import Chord
from note import Note
from harmonic_web import HarmonicWeb
import pprint

class CircleOfFifths(HarmonicWeb):
    def __init__(self, starting_chord=None):
        if starting_chord is None:
            midinote_numbers = [0, 4, 7]
        else:
            midinote_numbers = [note.midi_note_number for note in starting_chord.notes]

        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord

        # initializes the riemannian web map and constructs it with the helper function.
        self.web = {}
        self.build_web()

        # Initializes dict for when search paths are called
        self.breadth_first_path = {}

    def build_web(self, chord=None):
        """
        Builds the Riemannian web
        :param chord: default builds the web around the starting chord, but any triad that works in a Riemannian
        web can be given over as well.
        """
        if chord is None:
            chord = self.starting_chord
        # neighbors = self.get_neighbor_chords(chord)
        self.web[chord] = self.get_neighbor_chords(chord)
        for next_chord in self.web[chord]:
            if next_chord in self.web.keys():
                pass
            else:
                self.build_web(next_chord)

    def get_neighbor_chords(self, chord):
        # notes = [note.midi_note_number for note in chord]
        chords = [
            Chord(*[Note((note.midi_note_number + 7) % 12) for note in chord.notes]),
            Chord(*[Note((note.midi_note_number - 7) % 12) for note in chord.notes])
        ]
        return chords


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    e_major = Chord(Note(4), Note(8), Note(11))
    c_sharp_major = Chord(Note(1), Note(5), Note(8))
    circle_of_fifths = CircleOfFifths()
    # print(circle_of_fifths.get_neighbor_chords(c_major))
    circle_of_fifths.build_web()
    # print(circle_of_fifths.web)
    # pprint.pprint(circle_of_fifths.web)
    print("Printing shortest riemannian path between C Major and c#-minor")
    print(circle_of_fifths.breadth_first_search(c_sharp_major))
    print("Printing shortest riemannian path between c#-minor and e_minor")
    print(circle_of_fifths.breadth_first_search(e_major))
    print("Printing a random walk of 5 chords through the web with only new chords")
    print(circle_of_fifths.random_walk_only_new(5))
    print("Printing a truly random walk of 10 chords through the web")
    print(circle_of_fifths.true_random_walk(10))
