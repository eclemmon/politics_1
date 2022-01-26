
s = Server.default.boot;
Server.default.options.inDevice_("ZoomAudioD");
Server.default.options.outDevice_("ZoomAudioD");
~netaddress = NetAddr.new("127.0.0.1", 57120)
OSCFunc.trace(false);
(

SynthDef(\Q, {
	arg midi=48, speed=3, out=0, busout=99, gate=0, amp=0.2;
	var env = Env.perc;
	var envgen = EnvGen.kr(env, gate, doneAction: Done.freeSelf);
	var sin = SinOsc.ar((midi%12+60).midicps, 0.5);
	var sig = sin * envgen * amp;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.5);
	Out.ar([out, busout], pan);
}).add;

SynthDef(\delay1, {
	arg delaytime=0.6, out=0, in=99;
	var input = In.ar(in, 2);
	var effect = DelayN.ar(input, delaytime, delaytime, 0.2);
	Out.ar(out, effect);
}).add;

SynthDef(\delay2, {
	arg delaytime=0.8, out=0, in=99;
	var input = In.ar(in, 2);
	var effect = DelayN.ar(input, delaytime, delaytime, 0.05);
	Out.ar(out, effect);
}).add;

SynthDef(\reverb, {
	arg out=0, mix=0.25, room=0.15, damp=0.5, amp=1.0, in=0;
	var input, signal;
	input = In.ar(in, 2);
	signal = FreeVerb2.ar(input[0], input[1], mix, room, damp, amp);
	Out.ar(out, signal);
}).add;

(
// OSC FUNC WITH Pseq?
~delay1 = Synth(\delay1, [\in, 99]);
~delay2 = Synth(\delay2, [\in, 99]);
~reverb = Synth(\reverb, [\in, 98, \amp, 1.0, \mix, 0.5, \room, 0.7, \damp, 0.9]);
);

~start = [48,52,55];
~p_chord = Array.newFrom(~start);
~l_chord = Array.newFrom(~start);
~r_chord = Array.newFrom(~start);
~q_chord = Array.newFrom(~start);


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