
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

