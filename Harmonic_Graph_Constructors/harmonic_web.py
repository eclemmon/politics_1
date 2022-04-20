from Classes.chord import Chord
from Classes.note import Note
from typing import Union
import random


class HarmonicWeb:
    """
    HarmonicWeb superclass. Essentially a graph with logic especially suited for manipulating notes and chords.
    """
    def __init__(self, starting_chord: Union[Chord, None] = None):
        """
        Initializes the harmonic web  If starting chord is given, makes a copy of the chord and
        brings it into a lower octave.
        :param starting_chord: Chord || None
        """
        if starting_chord is None:
            midinote_numbers = [0, 4, 7]
        else:
            midinote_numbers = [note.midi_note_number for note in starting_chord.notes]

        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord
        self.output_chord = self.current_chord

        # initializes the web map and constructs it with the helper function.
        self.web = {}
        self.build_web()

        # Initializes dict for when search paths are called
        self.breadth_first_path = {}

    def build_web(self, chord: Union[Chord, None] = None):
        """
        Template function for building the web.
        :param chord: Chord || None
        :return: None
        """
        pass

    def breadth_first_search(self, destination_chord, starting_chord: Union[Chord, None] = None):
        """
        Breadth first search implementation, starting chord is wherever the 'cursor' is pointing via self.current_chord.
        Walks through the web to find the shortest path to the destination chord. Returns an empty pitches if the
        destination is the current chord. Otherwise, memoizes and returns the shortest path between self.current_chord
        and destination chord.
        :param starting_chord: Chord || None
        :param destination_chord: Chord
        :return: List
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
        Template function for building permutations of a chord.
        :param chord: Chord || None
        :return: None
        """
        pass

    def get_valid_chords(self, chord: Union[Chord, None] = None):
        """
        Template function for getting valid chords
        :param chord: Chord || None
        :return: None
        """
        pass

    @staticmethod
    def tonal_invert_chord(chord: list):
        """
        Inverts the elements of a chord tonally.
        :param chord: a list that reflects the pitch classes of a triad
        :return: returns a new list, with the last element appended to the front of the list and transposed down
        and octave.
        """
        # TODO: Check on tonal inversion and refactor so it takes advantage of Chord class
        chord[-1] -= 12
        element = chord.pop()
        return [element] + chord

    @staticmethod
    def build_chord(pitches: list):
        """
        Builds a chord out of a list of midi note numbers
        :param pitches: list
        :return: Chord
        """
        # TODO: Refactor as probably unnecessary
        notes = [Note(note_number) for note_number in pitches]
        return Chord(*notes)

    def random_walk_only_new(self, length: int):
        """
        Randomly walks through the Harmonic graph based on closest chords without traversing chords already
        visited. Returns current chord if length is 0.
        :param length: int
        :return: Returns the path as a list.
        """
        if length == 0:
            return [self.current_chord]

        visited = [self.current_chord]
        path = []
        for _ in (range(length)):
            options = self.web[self.current_chord]
            new_options = []
            for option in options:
                if option not in visited:
                    new_options.append(option)
            next_chord = random.choice(new_options)
            path.append(next_chord)
            visited.append(next_chord)
            self.current_chord = next_chord
        return path

    def true_random_walk(self, length: int):
        """
        Randomly walks through the Harmonic graph based on closest chords. Can visit chords already visited.
        returns current chord if length is 0.
        :param length: int
        :return: list
        """
        if length == 0:
            return [self.current_chord]

        path = []
        for _ in (range(length)):
            options = self.web[self.current_chord]
            next_chord = random.choice(options)
            path.append(next_chord)
            self.current_chord = next_chord
        return path

    def get_neighbor_chords(self):
        """
        Helper function that gets the next chords in the graph.
        :return: list
        """
        return self.web[self.current_chord]