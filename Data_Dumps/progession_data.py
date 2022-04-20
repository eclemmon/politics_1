from Classes.chord_progression import ChordProgression
from Classes.chord import Chord
from Classes.note import Note

cybernetic_republic_progressions = {
    'doo-wop': ChordProgression([
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(9), Note(0), Note(4), Note(9)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(7), Note(11), Note(2), Note(7)),
    ]),
    'weaponized': ChordProgression([
        Chord(Note(9), Note(0), Note(4), Note(9)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(0), Note(4), Note(7), Note(0)),
        Chord(Note(7), Note(11), Note(2), Note(7))
    ]),
    'pachelbel': ChordProgression([
        Chord(Note(0), Note(7), Note(0), Note(3)),
        Chord(Note(7), Note(7), Note(11), Note(2)),
        Chord(Note(9), Note(4), Note(9), Note(0)),
        Chord(Note(4), Note(4), Note(7), Note(11)),
        Chord(Note(5), Note(0), Note(5), Note(9)),
        Chord(Note(0), Note(0), Note(4), Note(7)),
        Chord(Note(9), Note(0), Note(2), Note(5)),
        Chord(Note(7), Note(11), Note(2), Note(5))
    ]),
    'lament': ChordProgression([
        Chord(Note(0), Note(3), Note(7)),
        Chord(Note(11), Note(7), Note(2)),
        Chord(Note(10), Note(7), Note(0), Note(3)),
        Chord(Note(9), Note(5), Note(0)),
        Chord(Note(8), Note(3), Note(0), Note(6)),
        Chord(Note(7), Note(3), Note(0)),
        Chord(Note(7), Note(2), Note(11), Note(5))
    ]),
    'changes': ChordProgression([
        Chord(Note(4), Note(7), Note(11), Note(2)),  # Em7
        Chord(Note(5), Note(9), Note(0), Note(3)),  # F7
        Chord(Note(10), Note(2), Note(5), Note(9)),  # BbMM7
        Chord(Note(1), Note(4), Note(8), Note(11)),  # Db7
        Chord(Note(6), Note(10), Note(1), Note(5)),  # GbMM7
        Chord(Note(9), Note(1), Note(4), Note(7)),  # A7
        Chord(Note(2), Note(6), Note(9), Note(1)),  # DMM7
        Chord(Note(2), Note(5), Note(9), Note(0)),  # Dmm7
    ]),
    'giant-steps': ChordProgression([
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
    'norm-core': ChordProgression([
        Chord(Note(12), Note(16), Note(19), Note(24)),
        Chord(Note(7), Note(16), Note(19), Note(24)),
        Chord(Note(12), Note(16), Note(19), Note(24)),
        Chord(Note(7), Note(16), Note(19), Note(24)),
        Chord(Note(12), Note(16), Note(19), Note(24)),
        Chord(Note(7), Note(16), Note(19), Note(24)),
        Chord(Note(12), Note(16), Note(19), Note(24)),
        Chord(Note(7), Note(16), Note(19), Note(24)),
    ])
}

cybernetic_republic_intro_progression = {
    'introduction': ChordProgression([
        Chord(Note(0), Note(4), Note(7)),
        Chord(Note(0), Note(4), Note(7)),
        Chord(Note(0), Note(4), Note(7)),
        Chord(Note(0), Note(5), Note(9))
    ])
}

