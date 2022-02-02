
s = Server.default.boot;
Server.default.options.inDevice_("ZoomAudioD");
Server.default.options.outDevice_("ZoomAudioD");
~netaddress = NetAddr.new("127.0.0.1", 57120)
OSCFunc.trace(false);


OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.do({arg item, i; [i, item].postln});
	"######################################".postln;
}, '/sound_triggers');


OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	"######################################".postln;
}, '/sound_triggers');

// HELPER FOR CONSTRUCTING
~bufs = ~makeWtBuffers.value()
Synth(\wavetable, [\freq, 50.midicps, \buf, ~bufs[0].bufnum, \numbufs, ~bufs.size, \gate, 1, \dur, 9, \amp, 0.1]);

Synth(\saw, [\gate, 1, \dur, 0.5, \freq, rrand(30,60).midicps, \amp, 0.1, \mAmp, 30, \mFreq, 2]);

Synth(\square, [\freq, 36.midicps, \mFreq, 0.2, \mAmp, 0.9, \dur, 5, \gate, 1]);

/*
[
OSC NAME
'/sound_triggers',
DELAY Feedback Delay Time, Delay Decay — 2 VALUES
15, 8,

REVERB predelay, reverbtime, lpf, mix — 4 VALUES
0.0, 0.9383333325386, 0.061666667461395, 0.1203999966383,

SPATIALIZATION Time Interval, Start Point, Target — 3 VALUES
6.5357141494751, 0.1203999966383, 0.0,

MODULATION Freq, Amp — 2 VALUES
0.0, 0.0,

OCTAVE — 1 VALUE
1,

TIME INTERVAL DATA
6.5357141494751,

INSTRUMENT NAMES — VAR VALUES
4, 'square', 'sin', 'impulse', 'sin',

WEIGHT OF CHORDS, SIZE OF CHORDS AND NOTES — VAR VALUES
0.6691871881485, 3.0, 4.0, 7.0, 11.0, 0.49402922391891, 3.0, 1.0, 5.0, 10.0, 0.83678364753723, 3.0, 1.0, 6.0, 9.0,

RHYTHM
1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5 ]
*/

OSCFunc({ |args|
	var triggers_queue, triggers_pitches, pitch_list, timing, triggers, trigger_timing, routine;
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postln;
	args.removeAt(0);
	timing = args.pop;
	"Trigger Queue".postln;
	triggers = List.new();
	triggers.addAll(args);
	triggers.postln;
	pitch_list = List.new();
	args.size.do {
		pitch_list.add(~q_chord.choose);
	};
	pitch_list.postln;
	triggers_pitches = Pseq(pitch_list, 1).asStream;
	triggers_queue = Pseq(triggers, 1).asStream;
	trigger_timing = Pseq(List.fill(args.size, { arg i; 1 }), 1).asStream;


	routine = Routine.new(
		{
			args.size.do {
				Synth(\Q, [\midi, triggers_pitches.next, \gate, triggers_queue.next]);
				// Synth(\Q, [\gate, triggers_queue.next]);
				(trigger_timing.next/10).yield;
			};
	}).play;

	"######################################".postln;
}, '/sound_triggers');

// OSC FUNCTION FOR HARMONIC TRIGGERS
OSCFunc({ |args|
	var harmonic_rhythm, timings_queue, pitches_queue, num_chords, timing, dur;
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postln;
	args.removeAt(0);
	harmonic_rhythm = args.removeAt(0);
	"Harmonic Rhythm:".postln;
	harmonic_rhythm.postln;
	num_chords = (harmonic_rhythm / args[0]).floor.asInteger;
	"Number of Chords:".postln;
	num_chords.postln;
	timings_queue = List.new();
	timing = args.removeAt(0);
	num_chords.do( { arg i; timings_queue.add(timing) });
	"Timings Queue:".postln;
	timings_queue.postln;

	dur = Pseq(timings_queue).asStream;

	~q_task = Task({
		var delta;
		while {
			delta = dur.next;
			delta.notNil;
		} {
			// args.postln;
			3.do( {arg i; ~q_chord.put(i, args.removeAt(0))} );
			3.do( {arg i; ~l_chord.put(i, args.removeAt(0))} );
			3.do( {arg i; ~p_chord.put(i, args.removeAt(0))} );
			3.do( {arg i; ~r_chord.put(i, args.removeAt(0))} );
			~q_chord.postln;
			delta.wait;
		};
		delta.yield;
	};

	).play;
	"######################################".postln;
}, '/harmonic_materials');


OSCFunc({ |args|
	var triggers_queue, triggers_pitches, pitch_list, timing, triggers, trigger_timing, routine;
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postln;
	args.removeAt(0);
	timing = args.pop;
	"Trigger Queue".postln;
	triggers = List.new();
	triggers.addAll(args);
	triggers.postln;
	pitch_list = List.new();
	args.size.do {
		pitch_list.add(~q_chord.choose);
	};
	pitch_list.postln;
	triggers_pitches = Pseq(pitch_list, 1).asStream;
	triggers_queue = Pseq(triggers, 1).asStream;
	trigger_timing = Pseq(List.fill(args.size, { arg i; 1 }), 1).asStream;


	routine = Routine.new(
		{
			args.size.do {
				Synth(\Q, [\midi, triggers_pitches.next, \gate, triggers_queue.next]);
				// Synth(\Q, [\gate, triggers_queue.next]);
				(trigger_timing.next/10).yield;
			};
	}).play;

	"######################################".postln;
}, '/pitch_triggers');

)

