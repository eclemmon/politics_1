from Classes.meter import SimpleDuple
from Classes.meter import SimpleTriple
from Classes.meter import ComplexMeter
from Classes.meter import CompoundMeter
from itertools import chain


def rr(i):
    """
    Helper function that returns a range of rests as a list
    :param i: Integer of number of rests
    :return: List of strings that represent rests
    """
    return ['/r' for _ in range(i)]


def nr(i, note_length=0.25):
    """
    Helper function that returns a range of notes as a list
    :param i: Integer of number of notes
    :param note_length: Float of length of note value — should be in multiples of 0.25
    :return: List of floats that represent note values
    """
    return [note_length for _ in range(i)]

class RhythmSection:
    def __init__(self, meter, midi_note_arrays=None, midi_note_duration_arrays=None):
        self.meter = meter
        self.midi_notes = midi_note_arrays
        self.midi_note_duration_arrays = midi_note_duration_arrays

    def transform_rhythm_to_meter(self):
        if self.meter.num_beats == 2:
            self.rhythm_to_duple()
        elif self.meter.num_beats == 3:
            self.rhythm_to_triple()
        elif self.meter.num_beats == 4:
            self.rhythm_to_four()
        elif self.meter.num_beats == 5:
            self.rhythm_to_five()
        elif self.meter.num_beats == 6:
            self.rhythm_to_six()
        elif self.meter.num_beats == 7:
            self.rhythm_to_seven()
        elif self.meter.num_beats == 9:
            self.rhythm_to_nine()
        elif self.meter.num_beats == 12:
            self.rhythm_to_twelve()
        else:
            pass

    def rhythm_to_duple(self):
        pass

    def rhythm_to_triple(self):
        pass

    def rhythm_to_four(self):
        pass

    def rhythm_to_five(self):
        pass

    def rhythm_to_six(self):
        pass

    def rhythm_to_seven(self):
        pass

    def rhythm_to_nine(self):
        pass

    def rhythm_to_twelve(self):
        pass

    def flatten(t):
        return [item for sublist in t for item in sublist]

    def build_new_midi_note_duration_array(self, *slices):
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = []
            for sl in slices:
                new_array = new_array + array[sl]
            new_midi_note_durations_array.append(new_array)
        return new_midi_note_durations_array



class BreakBeat(RhythmSection):
    def __init__(self, meter, option=2):
        super().__init__(meter)
        if option == 1:
            self.midi_notes = [i for i in range(60, 68)]
            self.midi_note_duration_arrays = [
                [0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', '/r', 0.25, '/r', 0.25,
                 '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r', '/r', 0.25, '/r', 0.25, '/r',
                 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25,
                 '/r', '/r', '/r', 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r'],
                [0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25 , '/r',
                 '/r', '/r', 0.25, 0.25, 0.25, '/r', '/r', '/r', 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25,
                 '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', '/r',
                 0.25, 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', 0.25],
                ['/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r',
                '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', 0.25,
                 '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r'],
                ['/r', '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r',
                 '/r', '/r', '/r', '/r', 0.25, '/r', '/r', '/r', '/r', '/r', '/r', '/r', '/r'],
                ['/r' for _ in range(4*4+1)] + [0.25, '/r', '/r', '/r', '/r', '/r', '/r', 0.25] +
                ['/r' for _ in range(9*4+3)],
                ['/r' for _ in range(5*4+3)] + [0.25] + ['/r' for _ in range(10*4)],
                [0.25] + ['/r' for _ in range(6*4+1)] + [0.25] + ['/r' for _ in range(3*4+3)] + [0.25, 0.25] +
                ['/r' for _ in range(4)] + [0.25, 0.25] + ['/r', '/r', '/r'] + [0.25, 0.25] + ['/r', '/r', '/r'] +
                [0.25, 0.25] + ['/r', '/r', '/r'] + [0.25],
                ['/r' for _ in range(4)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] +
                [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(9)] +
                [0.25] + [0.25]
            ]
        else:
            self.midi_notes = [i for i in range(36, 42)]
            self.midi_note_duration_arrays = [
                [0.25, '/r', 0.25] + ['/r' for _ in range(3)] + [0.25, 0.25, '/r', 0.25, 0.25, 0.25, '/r', '/r', 0.25,
                '/r', 0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25] + ['/r' for _ in range(4)] + [0.25,
                '/r', 0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, 0.25, '/r', 0.25] + ['/r' for _ in range(5)] + [0.25,
                0.25, '/r', 0.25, '/r', '/r', '/r', 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, '/r', '/r', '/r'],
                ['/r' for _ in range(4)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] +
                [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(9)] +
                [0.25, 0.25],
                [0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] +
                [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25,
                '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25, 0.25, '/r'] + [0.25, 0.25,
                0.25, '/r'] + [0.25, 0.25, 0.25, '/r', '/r'] + [0.25, 0.25, '/r', '/r', 0.25, 0.25, '/r', 0.25, 0.25,
                0.25, '/r', 0.25],
                ['/r' for _ in range(6)] + [0.25] + ['/r' for _ in range(15)] + [0.25] + ['/r' for _ in range(15)] +
                [0.25] + ['/r' for _ in range(16)] + [0.25] + ['/r' for _ in range(8)],
                ['/r', '/r', 0.25] + ['/r' for _ in range(7)] + [0.25] + ['/r' for _ in range(7)] + [0.25] +
                ['/r' for _ in range(15)] + [0.25] + ['/r' for _ in range(11)] + [0.25] + ['/r' for _ in range(3)] +
                [0.25] + ['/r' for _ in range(11)] + [0.25, '/r'],
                ['/r' for _ in range(6*4+2)] + [0.25] + ['/r' for _ in range(15)] + [0.25, 0.25] +
                ['/r' for _ in range(4)] + [0.25, '/r', '/r', 0.25, '/r', '/r', 0.25, '/r', '/r', 0.25, '/r', '/r',
                                            0.25, 0.25, 0.25, 0.25]
            ]

        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        new_midi_note_durations_array = []
        for array in self.midi_note_duration_arrays:
            new_array = array[0:8] + array[16:24] + array[32:40] + array[56:64]
            new_midi_note_durations_array.append(new_array)
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_triple(self):
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 12), slice(16, 28),
                                                                               slice(0, 12), slice(16, 28))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_five(self):
        if self.meter.subdivisions == [2, 3]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(16, 22),
                                                                                    slice(0, 4), slice(16, 22))
        else:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(20, 24),
                                                                                    slice(0, 6), slice(60, 64))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_six(self):
        new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(0, 6),
                                                                                slice(6, 12), slice(0, 6))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                    slice(0, 6))
        elif self.meter.subdivisions == [2, 3, 2]:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 4), slice(0, 6),
                                                                                    slice(6, 10))
        else:
            new_midi_note_durations_array = self.build_new_midi_note_duration_array(slice(0, 6), slice(0, 4),
                                                                                    slice(6, 10))
        self.midi_note_duration_arrays = new_midi_note_durations_array

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6), slice(0, 6))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(6, 12), slice(0, 6),
                                                                                 slice(0, 6), slice(0, 6))


class CompoundSix(RhythmSection):
    def __init__(self, meter):
        super().__init__(meter)
        self.midi_notes = [midi_note for midi_note in range(44, 48)]
        self.midi_note_duration_arrays = [
            [0.25] + rr(11) + [0.25] + rr(9) + [0.25, '/r', 0.25] + rr(11) + [0.25] + rr(5) + [0.25] + rr(3) +
            [0.25, '/r'],
            rr(5) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(2) + [0.25] + rr(3),
            list(chain.from_iterable([[0.25, '/r'] for _ in range(24)])),
            rr(6) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(11) + [0.25] + rr(2) + [0.25] + rr(2)
        ]
        self.transform_rhythm_to_meter()

    def rhythm_to_duple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_triple(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 9), slice(5, 10),
                                                                                 slice(0, 3), slice(5, 9), slice(41, 44),
                                                                                 slice(2, 4))

    def rhythm_to_four(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 4), slice(6, 10), slice(0, 4),
                                                                                 slice(6, 10), slice(0, 4), slice(6, 10),
                                                                                 slice(36, 37), slice(41, 48))

    def rhythm_to_five(self):
        if self.meter.subdivisions == [2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 12),
                                                                                     slice(0, 3), slice(17, 24))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 10), slice(0, 8),
                                                                                     slice(22, 24))

    def rhythm_to_seven(self):
        if self.meter.subdivisions == [2, 2, 3]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 9),
                                                                                     slice(5, 12), slice(0, 3),
                                                                                     slice(5, 9), slice(17, 24))
        elif self.meter.subdivisions == [2, 3, 2]:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 3), slice(5, 11),
                                                                                     slice(5, 9))
        else:
            self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 9), slice(5, 10))

    def rhythm_to_nine(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11), slice(5, 12),
                                                                                 slice(0, 11), slice(41, 48))

    def rhythm_to_twelve(self):
        self.midi_note_duration_arrays = self.build_new_midi_note_duration_array(slice(0, 11),  slice(5, 11),
                                                                                 slice(17, 24), slice(0, 11),
                                                                                 slice(5, 11), slice(41, 48))


if __name__ == "__main__":
    from pythonosc import udp_client
    from pythonosc import osc_message_builder

    sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    meter = SimpleDuple(4)
    duplemeter = SimpleDuple(2)
    triplemeter = SimpleTriple()
    threetwo = ComplexMeter(5, [3, 1, 1, 2, 1], [3, 2])
    twothree = ComplexMeter(5, [3, 1, 2, 1, 1], [2, 3])
    twotwothree = ComplexMeter(7, [3, 1, 2, 1, 2, 1, 1], [2, 2, 3])
    twothreetwo = ComplexMeter(7, [3, 1, 2, 1, 1, 2, 1], [2, 3, 2])
    threetwotwo = ComplexMeter(7, [3, 1, 1, 2, 1, 2, 1], [3, 2, 2])
    six = CompoundMeter(6, [3, 1, 1, 2, 1, 1], [3, 3])
    nine = CompoundMeter(9, [3, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3])
    twelve = CompoundMeter(12, [3, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1], [3, 3, 3, 3])
    bb = BreakBeat(meter)
    bb2beats = BreakBeat(duplemeter)
    bb3beats = BreakBeat(triplemeter)
    bbtwothree = BreakBeat(twothree)
    bbthreetwo = BreakBeat(threetwo)
    bbsix = BreakBeat(six)
    bbtwotwothree = BreakBeat(twotwothree)
    bbtwothreetwo = BreakBeat(twothreetwo)
    bbthreetwotwo = BreakBeat(threetwotwo)
    bbnine = BreakBeat(nine)
    bbtwelve = BreakBeat(twelve)

    cc = CompoundSix(six)
    cc2 = CompoundSix(duplemeter)
    cc3 = CompoundSix(triplemeter)
    cc4 = CompoundSix(meter)
    cc23 = CompoundSix(twothree)
    cc32 = CompoundSix(threetwo)
    cc223 = CompoundSix(twotwothree)
    cc232 = CompoundSix(twothreetwo)
    cc322 = CompoundSix(threetwotwo)
    cc9 = CompoundSix(nine)
    cc12 = CompoundSix(twelve)

    def send_to_sc(rhythm_section, address="/break_beat_1"):
        for i in range(len(rhythm_section.midi_notes)):
            msg = osc_message_builder.OscMessageBuilder(address=address)
            msg.add_arg(rhythm_section.midi_notes[i], 'i')
            for note_event in rhythm_section.midi_note_duration_arrays[i]:
                msg.add_arg(note_event)
            msg = msg.build()
            sc_client.send(msg)

        msg = osc_message_builder.OscMessageBuilder(address="/init")
        msg.add_arg("break_beat_1")
        msg.add_arg("rhythm")
        msg = msg.build()
        sc_client.send(msg)

    # send_to_sc(bb)
    # send_to_sc(bb2beats)
    # send_to_sc(bb3beats)
    # send_to_sc(bbthreetwo)
    # send_to_sc(bbtwothree)
    # send_to_sc(bbsix)
    # send_to_sc(bbthreetwotwo)
    # send_to_sc(bbtwothreetwo)
    # send_to_sc(bbtwotwothree)
    # send_to_sc(bbnine)
    # send_to_sc(bbtwelve)
    send_to_sc(cc12)
    # for i in range(len(bb.midi_notes)):
    #     msg = osc_message_builder.OscMessageBuilder(address="/break_beat_1")
    #     msg.add_arg(bb.midi_notes[i], 'i')
    #     for note_event in bb.midi_note_duration_arrays[i]:
    #         msg.add_arg(note_event)
    #     msg = msg.build()
    #     sc_client.send(msg)
    #
    # msg = osc_message_builder.OscMessageBuilder(address="/init")
    # msg.add_arg("break_beat_1")
    # msg.add_arg("rhythm")
    # msg = msg.build()
    # sc_client.send(msg)