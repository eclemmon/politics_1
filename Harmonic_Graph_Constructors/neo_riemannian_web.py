from Classes.chord import Chord
from Classes.note import Note
from itertools import permutations
from Harmonic_Graph_Constructors import harmonic_web
from typing import Union


class NeoriemannianWeb(harmonic_web.HarmonicWeb):
    """
    NeoriemannianWeb class. A graph that reflects the cyclical and pitch-based relationships between triads in
    neo-Riemannian theory.
    """
    def __init__(self, starting_chord: Union[Chord, None] = None):
        """
        Initializes the NeoriemannianWeb
        :param starting_chord: Chord || None
        """
        if starting_chord is None:
            midinote_numbers = [0, 4, 7]
        else:
            midinote_numbers = [note.midi_note_number for note in starting_chord.notes]

        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord
        self.output_chord = self.current_chord

        # initializes the riemannian web map and constructs it with the helper function.
        self.web = {}
        self.build_web()

        # Initializes dict for when search paths are called
        self.breadth_first_path = {}

    def build_web(self, chord: Union[Chord, None] = None):
        """
        Builds the Riemannian web. Default builds the web around the starting chord, but any triad that works
        in a Riemannian graph can be given over as well.
        :param chord: Chord
        """
        if chord is None:
            chord = self.starting_chord
        neighbors = self.get_valid_chords(chord)
        self.web[chord] = [self.build_chord(neighbor) for neighbor in neighbors]
        for next_chord in self.web[chord]:
            if next_chord in self.web.keys():
                pass
            else:
                self.build_web(next_chord)

    def breadth_first_search(self, destination_chord: Chord, starting_chord: Union[Chord, None] = None):
        """
        Breadth first search implementation, starting chord is wherever the 'cursor' is pointing via self.current_chord.
        walks through the web to find the shortest path to the destination chord. Returns and empty array if the
        destination is the current chord. Otherwise, memoizes and returns the shortest path between self.current_chord
        and destination chord.
        :param starting_chord: Chord || None
        :param destination_chord: Chord
        :return: list
        """
        if starting_chord is None:
            starting_chord = self.current_chord
        visited = []
        queue = [[starting_chord]]

        if starting_chord == destination_chord:
            return [destination_chord]

        if (starting_chord, destination_chord) in self.breadth_first_path.keys():
            substitute_chord = self.current_chord
            self.current_chord = destination_chord
            return self.breadth_first_path[(substitute_chord, destination_chord)]

        while queue:
            path = queue.pop(0)
            chord = path[-1]
            if chord not in visited:
                child_chords = self.web[chord]

                for child_chord in child_chords:
                    new_path = list(path)
                    new_path.append(child_chord)
                    queue.append(new_path)
                    if child_chord == destination_chord:
                        self.breadth_first_path[(self.current_chord, destination_chord)] = new_path
                        self.current_chord = destination_chord
                        return new_path

                visited.append(chord)

        return []

    def build_chord_permutations(self, chord: Union[Chord, None] = None):
        """
        neo-Riemannian chords are typically triads. To figure out the neighbor chords agnostically to the asymmetry
        between pitch classes and the triadic system, this helper function builds all possible permutations of a chord's
        altered notes by whole- and half-step. Returns a list of permutations of all chords possible after altering the
        initial chord by half- or whole-step.
        :param chord: Chord || None
        :return: list
        """
        if chord is None:
            chord = self.starting_chord
        perms = []
        midi_note_numbers = [note.midi_note_number for note in chord.notes]
        for index, note in enumerate(midi_note_numbers):
            new_chord1 = midi_note_numbers.copy()
            new_chord2 = midi_note_numbers.copy()
            new_chord3 = midi_note_numbers.copy()
            new_chord4 = midi_note_numbers.copy()
            new_chord1[index] = note + 1
            new_chord2[index] = note - 1
            new_chord3[index] = note + 2
            new_chord4[index] = note - 2
            chords = [new_chord1, new_chord2, new_chord3, new_chord4]
            for i, chord in enumerate(chords):
                chords[i] = [note % 12 for note in chord]
                perms += permutations(chords[i])
        perms = [list(t) for t in perms]
        return perms

    def get_valid_chords(self, chord: Union[Chord, None] = None):
        """
        This takes in a chord and returns all valid neighbor chords in a neo-Riemannian web. If the starting chord is
        none, the starting chord will be self.starting_chord via the build_chord_permutations call. Returns a list of
        valid neighbor chords in a neo-Riemannian web.
        :param chord: Chord
        :return: list
        """
        valid_chords = []
        chords = self.build_chord_permutations(chord)
        for chord in chords:
            rotation1 = self.tonal_invert_chord(chord.copy())
            rotation2 = self.tonal_invert_chord(rotation1.copy())
            inversions = [chord, rotation1, rotation2]
            for inversion in inversions:
                if inversion[2] - inversion[0] == 7:
                    if inversion[1] - inversion[0] == 3 or inversion[1] - inversion[0] == 4:
                        valid_chords.append(chord)

        return valid_chords


if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    e_minor = Chord(Note(4), Note(7), Note(11))
    c_sharp_minor = Chord(Note(1), Note(4), Note(8))
    web = NeoriemannianWeb(c_major)
    web2 = NeoriemannianWeb(e_minor)
    # print(web.get_valid_chords())
    # web.build_chord_permutations()
    # print(web.build_chord([4, 7, 11]))
    web.build_web()
    # print(web.web.keys())
    # print(web.web)
    # pprint.pprint(web.web)
    print("Printing shortest riemannian path between C Major and c#-minor")
    print(web.breadth_first_search(c_sharp_minor))
    print("Printing shortest riemannian path between c#-minor and e_minor")
    print(web.breadth_first_search(e_minor))
    print("Printing a random walk of 5 chords through the web with only new chords")
    print(web.random_walk_only_new(5))
    print("Printing a truly random walk of 10 chords through the web")
    print(web.true_random_walk(10))
    print("current chord")
    print(web.current_chord)
    print("getting neighbor chords")
    print(web.get_neighbor_chords())
