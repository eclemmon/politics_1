from chord import Chord
from note import Note
from itertools import permutations
import random
import pprint


class Neoriemannian_web:
    def __init__(self, starting_chord):

        midinote_numbers = [note.midi_note_number for note in starting_chord.notes]
        self.starting_chord = Chord(*[Note(note % 12) for note in midinote_numbers])
        self.current_chord = self.starting_chord

        self.web = {}
        self.build_web()

        self.breadth_first_path = {}
        self.depth_first_path = {}

    def build_web(self, chord=None):
        if chord == None:
            chord = self.starting_chord
        neighbors = self.get_valid_chords(chord)
        self.web[chord] = [self.build_chord(neighbor) for neighbor in neighbors]
        for next_chord in self.web[chord]:
            if next_chord in self.web.keys():
                pass
            else:
                self.build_web(next_chord)

    def breadth_first_search(self, destination_chord):
        visited = []
        queue = [[self.current_chord]]

        if self.current_chord == destination_chord:
            return [destination_chord]

        if (self.current_chord, destination_chord) in self.breadth_first_path.keys():
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

    def depth_first_search(self, destination_chord):
        pass

    def build_chord_permutations(self, chord=None):
        if chord is None:
            chord = self.starting_chord
        perms = []
        midinote_numbers = [note.midi_note_number for note in chord.notes]
        for index, note in enumerate(midinote_numbers):
            new_chord1 = midinote_numbers.copy()
            new_chord2 = midinote_numbers.copy()
            new_chord3 = midinote_numbers.copy()
            new_chord4 = midinote_numbers.copy()
            new_chord1[index] = note+1
            new_chord2[index] = note-1
            new_chord3[index] = note+2
            new_chord4[index] = note-2
            chords = [new_chord1, new_chord2, new_chord3, new_chord4]
            for i, chord in enumerate(chords):
                chords[i] = [note % 12 for note in chord]
                perms += permutations(chords[i])
        perms = [list(t) for t in perms]
        return perms

    def get_valid_chords(self, chord=None):
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

    @staticmethod
    def tonal_invert_chord(chord):
        chord[-1] -= 12
        element = chord.pop()
        return [element] + chord

    @staticmethod
    def build_chord(array):
        notes = [Note(note_number) for note_number in array]
        return Chord(*notes)

    def random_walk_only_new(self, length):
        visited = [self.current_chord]
        path = []
        for time in (range(length)):
            options = self.web[self.current_chord]
            new_options = []
            for option in options:
                if option not in visited:
                    new_options.append(option)
            next_chord = random.choice(new_options)
            path.append(next_chord)
            self.current_chord = next_chord
        return path

    def true_random_walk(self, length):
        path = []
        for time in (range(length)):
            options = self.web[self.current_chord]
            next_chord = random.choice(options)
            path.append(next_chord)
            self.current_chord = next_chord
        return path




if __name__ == '__main__':
    c_major = Chord(Note(60), Note(64), Note(67))
    e_minor = Chord(Note(4), Note(7), Note(11))
    c_sharp_minor = Chord(Note(1), Note(4), Note(8))
    web = Neoriemannian_web(c_major)
    web2 = Neoriemannian_web(e_minor)
    # print(web.get_valid_chords())
    # web.build_chord_permutations()
    # print(web.build_chord([4, 7, 11]))
    web.build_web()
    # print(web.web.keys())
    # print(web.web)
    pprint.pprint(web.web)
    print("Printing shortest riemannian path between C Major and c#-minor")
    print(web.breadth_first_search(c_sharp_minor))
    print("Printing shortest riemannian path between c#-minor and e_minor")
    print(web.breadth_first_search(e_minor))
    print("Printing a random walk of 5 chords through the web with only new chords")
    print(web.random_walk_only_new(5))
    print("Printing a truly random walk of 10 chords through the web")
    print(web.true_random_walk(10))
