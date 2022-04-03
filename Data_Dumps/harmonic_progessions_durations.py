from Classes.harmony import Harmony
from Classes.chord import Chord
from Classes.note import Note

cybernetic_republic_harmonic_progressions = {
    'doo-wop': Harmony([
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(9), Note(0), Note(4), Note(9)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(7), Note(11), Note(2), Note(7)),
    ]),
    'weaponized': Harmony([
        Chord(Note(9), Note(0), Note(4), Note(9)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(11), Note(2), Note(7))
    ]),
    'pachelbel': Harmony([
        Chord(Note(0), Note(7), Note(0), Note(3)),
        Chord(Note(7), Note(7), Note(11), Note(2)),
        Chord(Note(9), Note(4), Note(9), Note(0)),
        Chord(Note(4), Note(4), Note(7), Note(11)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(0), Note(0), Note(4), Note(7)),
        Chord(Note(9), Note(0), Note(2), Note(5)),
        Chord(Note(7), Note(11), Note(2), Note(5))
    ]),
    'chromatic-lament': Harmony([
        Chord(Note(0), Note(3), Note(7)),
        Chord(Note(11), Note(7), Note(2)),
        Chord(Note(10), Note(7), Note(0), Note(3)),
        Chord(Note(9), Note(5), Note(0)),
        Chord(Note(8), Note(3), Note(0), Note(6)),
        Chord(Note(7), Note(3), Note(0)),
        Chord(Note(7), Note(2), Note(11), Note(5))
    ]),
    'changes': Harmony([
        Chord(Note(4), Note(7), Note(11), Note(2)),  # Em7
        Chord(Note(5), Note(9), Note(0), Note(3)),  # F7
        Chord(Note(10), Note(2), Note(5), Note(9)),  # BbMM7
        Chord(Note(1), Note(4), Note(8), Note(11)),  # Db7
        Chord(Note(6), Note(10), Note(1), Note(5)),  # GbMM7
        Chord(Note(9), Note(1), Note(4), Note(7)),  # A7
        Chord(Note(2), Note(6), Note(9), Note(1)),  # DMM7
        Chord(Note(2), Note(5), Note(9), Note(0)),  # Dmm7
        Chord(Note(3), Note(7), Note(10), Note(1)),  # Eb7
        Chord(Note(8), Note(0), Note(3), Note(7)),  # AbMM7
        Chord(Note(11), Note(3), Note(6), Note(9)),  # B7
        Chord(Note(4), Note(8), Note(11), Note(3)),  # EMM7
        Chord(Note(7), Note(11), Note(2), Note(5)),  # G7
        Chord(Note(0), Note(4), Note(7), Note(11)),  # CMM7
    ]),
    'giant-steps': Harmony([
        Chord(Note(11), Note(3), Note(6), Note(10)),  # BMM7
        Chord(Note(2), Note(6), Note(9), Note(0)),  # D7
        Chord(Note(7), Note(11), Note(2), Note(5)),  # GMM7
        Chord(Note(10), Note(2), Note(5), Note(8)),  # Bb7
        Chord(Note(3), Note(7), Note(10), Note(2)),  # EbMM7
        Chord(Note(9), Note(0), Note(4), Note(7)),  # Amm7
        Chord(Note(2), Note(6), Note(9), Note(0)),  # D7
        Chord(Note(7), Note(11), Note(2), Note(5)),  # GMM7
        Chord(Note(10), Note(2), Note(5), Note(8)),  # Bb7
        Chord(Note(3), Note(7), Note(10), Note(2)),  # EbMM7
        Chord(Note(6), Note(10), Note(1), Note(4)),  # F#7
    ]),
    'norm-core': Harmony([
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(4), Note(7), Note(0)),
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(4), Note(7), Note(0)),
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(4), Note(7), Note(0)),
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(4), Note(7), Note(0)),
    ])
}



