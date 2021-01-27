s = Server.default.boot;
Server.default.options.outDevice_("Multi-Output Device");
~netaddress = NetAddr.new("127.0.0.1", 57120)
{ LPF.ar(Saw.ar(200,0.1), SinOsc.kr(1,0,3600,4000)) }.play;

(
// SYNTH DEFS HERE
SynthDef(\Q, {
	arg midi=48, speed=3, out=0, busout=99, gate=0;
	var env = Env.perc;
	var envgen = EnvGen.kr(env, gate);
	var sin = SinOsc.ar((midi%12+60).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.5);
	Out.ar([out, busout], pan);
}).add;


SynthDef(\L, {
	arg midi=48, speed=0.05, out=0, gate=0;
	var env = Env.new(
		levels: [0,1,0],
		times: [3,4]);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var saw = Saw.ar((midi%12+24).midicps, 1);
	var sin = SinOsc.ar((midi%12+24).midicps, 1);
	var sig = sin * saw * envgen;
	var filter = LPF.ar(sig, XLine.kr(50, 300, 7));
	var pan = Pan2.ar(filter, pos: SinOsc.kr(0.1), level: 1);
	Out.ar(out, pan);
}).add;

SynthDef(\P, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(releaseTime: 0.01);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+96).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.005);
	Out.ar(out, pan);
}).add;

SynthDef(\R, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(out, pan);
}).add;

SynthDef(\R2, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var noise = WhiteNoise.ar(0.1);
	var sig = sin * envgen * noise;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(out, pan);
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
)

(
// NEW SYNTH DEFS HERE
SynthDef(\Q, {
	arg midi=48, speed=3, out=0, busout=99, gate=0;
	var env = Env.perc;
	var envgen = EnvGen.kr(env, gate);
	var sin = SinOsc.ar((midi%12+60).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.5);
	Out.ar([out, busout], pan);
}).add;


SynthDef(\L, {
	arg midi=48, speed=0.05, out=0, gate=0;
	var env = Env.new(
		levels: [0,1,0],
		times: [3,4]);
	var envgen = EnvGen.kr(env, gate);
	var saw = Saw.ar((midi%12+24).midicps, 1);
	var sin = SinOsc.ar((midi%12+24).midicps, 1);
	var sig = sin * saw * envgen;
	var filter = LPF.ar(sig, XLine.kr(50, 300, 7));
	var pan = Pan2.ar(filter, pos: SinOsc.kr(0.1), level: 1);
	Out.ar(out, pan);
}).add;

SynthDef(\P, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(releaseTime: 0.01);
	var envgen = EnvGen.kr(env, gate);
	var sin = SinOsc.ar((midi%12+96).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.005);
	Out.ar(out, pan);
}).add;

SynthDef(\R, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, gate);
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(out, pan);
}).add;

SynthDef(\R2, {
	arg midi=48, speed=3, out=0, gate=0;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, gate);
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var noise = WhiteNoise.ar(0.1);
	var sig = sin * envgen * noise;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(out, pan);
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
)

(
(
// THIS ONE ADDS HAS A WORKING QUEUE
~delay1 = Synth(\delay1, [\in, 99]);
~delay2 = Synth(\delay2, [\in, 99]);
~reverb = Synth(\reverb, [\in, 98, \amp, 0.5, \mix, 0.5, \room, 0.7, \damp, 0.9]);
);

~start = [48,52,55];
~p_chord = Array.new(3);
~l_chord = Array.new(3);
~r_chord = Array.new(3);
~q_chord = Array.new(3);
~pitches_queue = List.new();
~timings_queue = List.new();
~triggers_queue = List.new();

~start.do({
	arg note, index;
	~q_chord.add(Synth(\Q, [\midi, note, \speed, (index+1)*0.3, \out, 98, \outbus, 99]););
	~l_chord.add(Synth(\L, [\midi, note, \speed, (index+1)*0.1, \out, 98]););
	~p_chord.add(Synth(\P, [\midi, note, \speed, (index+1)*4, \out, 0]););
	~r_chord.add(Synth(\R2, [\midi, note, \speed, (index+1)*0.4, \out, 98]););
});

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
			3.do( {arg i; ~q_chord[i].set(\midi, args.removeAt(0))});
			3.do( {arg i; ~l_chord[i].set(\midi, args.removeAt(0))});
			3.do( {arg i; ~p_chord[i].set(\midi, args.removeAt(0))});
			3.do( {arg i; ~r_chord[i].set(\midi, args.removeAt(0))});
			delta.wait;
		};
		delta.yield;
	};

).play;
	"######################################".postln;
}, '/harmonic_materials');


OSCFunc({ |args|
	var harmonic_rhythm, triggers_queue, pitches_queue, num_chords, timing, tiggers;
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postln;
	args.removeAt(0);
	timing = args.pop;
	"Trigger Queue".postln;
	~triggers_queue.addAll(args);
	~triggers_queue.postln;

	~trigger_task = Task({
		var delta, trigger_val;
		while {
			delta = timing;
			~triggers_queue.size != 0;
		} {
			// args.postln;
			trigger_val = ~triggers_queue.removeAt(0);
			trigger_val.postln;
			3.do( {arg i; ~q_chord[i].set(\gate, trigger_val)});
			(timing/5).wait;
		};
		delta.yield;
	};

).play;
	"######################################".postln;
}, '/pitch_triggers');


)



(
(
~delay1 = Synth(\delay1, [\in, 99]);
~delay2 = Synth(\delay2, [\in, 99]);
~reverb = Synth(\reverb, [\in, 98, \amp, 0.5, \mix, 0.5, \room, 0.7, \damp, 0.9]);
);

~start = [48,52,55];
~p_chord = Array.new(3);
~l_chord = Array.new(3);
~r_chord = Array.new(3);
~q_chord = Array.new(3);

~start.do({
	arg note, index;
	~q_chord.add(Synth(\Q, [\midi, note, \speed, (index+1)*0.3, \out, 98, \outbus, 99]););
	~l_chord.add(Synth(\L, [\midi, note, \speed, (index+1)*0.1, \out, 98]););
	~p_chord.add(Synth(\P, [\midi, note, \speed, (index+1)*4, \out, 0]););
	~r_chord.add(Synth(\R2, [\midi, note, \speed, (index+1)*0.4, \out, 98]););
});

OSCFunc({ |args|
	"OSCFUNC received the following values:".postln;
	args.postln;
	args[2..4].do {
		arg item, counter;
		~q_chord[counter].set(\midi, item);
	};
	args[6..8].do {
		arg item, counter;
		~l_chord[counter].set(\midi, item);
	};
	args[10..12].do {
		arg item, counter;
		~p_chord[counter].set(\midi, item);
	};
	args[14..16].do {
		arg item, counter;
		~r_chord[counter].set(\midi, item);
	};
}, '/harmonic_materials');
)



(
(
~delay1 = Synth(\delay1, [\in, 99]);
~delay2 = Synth(\delay2, [\in, 99]);
~reverb = Synth(\reverb, [\in, 98, \amp, 0.5, \mix, 0.5, \room, 0.7, \damp, 0.9]);
);

~start = [48,52,55];
~p_chord = Array.new(3);
~l_chord = Array.new(3);
~r_chord = Array.new(3);
~q_chord = Array.new(3);

~start.do({
	arg note, index;
	~q_chord.add(Synth(\Q, [\midi, note, \speed, (index+1)*0.3, \out, 98, \outbus, 99]););
	~l_chord.add(Synth(\L, [\midi, note, \speed, (index+1)*0.1, \out, 98]););
	~p_chord.add(Synth(\P, [\midi, note, \speed, (index+1)*4, \out, 0]););
	~r_chord.add(Synth(\R2, [\midi, note, \speed, (index+1)*0.4, \out, 98]););
});

~q_pitches = List.new();
~l_pitches = List.new();
~p_pitches = List.new();
~r_pitches = List.new();
~q_durations = List.new();
~l_durations = List.new();
~p_durations = List.new();
~r_durations = List.new();

OSCFunc({ |args|
	var dictionary;
	"OSCFUNC received the following values:".postln;

	// args.postln;
	~q_pitches.add(args[2..4]);
	~l_pitches.add(args[6..8]);
	~p_pitches.add(args[10..12]);
	~r_pitches.add(args[14..16]);
	~q_durations.add(args[18]);
	~l_durations.add(args[18]);
	~p_durations.add(args[18]);
	~r_durations.add(args[18]);
	~q_pitches.postln;
/*	~sequence_trigger.value(
		q_midi: ~q_pitches,
		l_midi: ~l_pitches,
		p_midi: ~p_pitches,
		r_midi: ~r_pitches,
		q_dur: ~q_durations,
		l_dur: ~l_durations,
		p_dur: ~p_durations,
		r_dur: ~r_durations);*/
	~sequence_trigger;
}, '/harmonic_materials');
)

(
var qmidi, lmidi, pmidi, rmidi, qdur, ldur, pdur, rdur;
qmidi = Pseq(~q_pitches).asStream;
qdur = Pseq(~q_duration).asStream;
lmidi = Pseq(~l_pitches).asStream;
ldur = Pseq(~l_durations).asStream;
pmidi = Pseq(~p_pitches).asStream;
pdur = Pseq(~p_durations).asStream;
rmidi = Pseq(~r_pitches).asStream;
rdur = Pseq(~r_durations).asStream;

~q_task = Task({
	var delta;
	while {
	delta = qdur.next;
	delta.notNil;
} {
	~q_pitches.postln;
	~q_pitches.removeAt(0).do {
		arg item, counter;
		~q_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~p_task = Task({
	var delta;
	while {
	delta = pdur.next;
	delta.notNil;
} {
	~p_pitches.removeAt(0).do {
		arg item, counter;
		~p_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~l_task = Task({
	var delta;
	while {
	delta = ldur.next;
	delta.notNil;
} {
	~l_pitches.removeAt(0).do {
		arg item, counter;
		~l_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~r_task = Task({
	var delta;
	while {
	delta = rdur.next;
	delta.notNil;
} {
	~r_pitches.removeAt(0).do {
		arg item, counter;
		~r_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}
).play;
)

(
~sequence_trigger = {
var qmidi, lmidi, pmidi, rmidi, qdur, ldur, pdur, rdur;
qmidi = Pseq(q_midi).asStream;
qdur = Pseq(q_dur).asStream;
lmidi = Pseq(l_midi).asStream;
ldur = Pseq(l_dur).asStream;
pmidi = Pseq(p_midi).asStream;
pdur = Pseq(p_dur).asStream;
rmidi = Pseq(r_midi).asStream;
rdur = Pseq(r_dur).asStream;

~q_task = Task({
	var delta;
	while {
	delta = qdur.next;
	delta.notNil;
} {
	q_midi.postln;
	q_midi.removeAt(0).do {
		arg item, counter;
		~q_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~p_task = Task({
	var delta;
	while {
	delta = pdur.next;
	delta.notNil;
} {
	p_midi.removeAt(0).do {
		arg item, counter;
		~p_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~l_task = Task({
	var delta;
	while {
	delta = ldur.next;
	delta.notNil;
} {
	l_midi.removeAt(0).do {
		arg item, counter;
		~l_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;

~r_task = Task({
	var delta;
	while {
	delta = rdur.next;
	delta.notNil;
} {
	r_midi.removeAt(0).do {
		arg item, counter;
		~r_chord[counter].set(\midi, item);
	};
	delta.yield;
	}
}).play;
})


