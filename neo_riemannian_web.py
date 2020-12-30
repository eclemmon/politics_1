class Neoriemannian_web:
    def __init__(self, starting_chord):
        self.starting_chord = starting_chord
        self.web = {}

    def build_web(self):
        edges = []