from Classes.note import Note
from Classes.scale import Scale

major = Scale(Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11))

cybernetic_republic_scales = {
    'major': major,
    'dorian': major.modal_transpose_return_new(2),
    'phrygian': major.modal_transpose_return_new(3),
    'lydian': major.modal_transpose_return_new(4),
    'mixolydian': major.modal_transpose_return_new(5),
    'aeolean': major.modal_transpose_return_new(6),
    'locrian': major.modal_transpose_return_new(7),
    'blues': Scale(Note(0), Note(2), Note(3), Note(4), Note(5), Note(7), Note(9), Note(10), Note(11)),
    'harmonic-minor': Scale(Note(0), Note(2), Note(3), Note(5), Note(7), Note(8), Note(11))
}