s = Server.default.boot;
Server.default.options.outDevice_("Multi-Output Device");
~netaddress = NetAddr.new("127.0.0.1", 57120)
{ LPF.ar(Saw.ar(200,0.1), SinOsc.kr(1,0,3600,4000)) }.play;

(
SynthDef(\Q, {
	arg midi=48, speed=3, out=0, busout=99;
	var env = Env.perc;
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+60).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.5);
	Out.ar([out, busout], pan);
}).add;

SynthDef(\L, {
	arg midi=48, speed=0.05, out=0;
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
	arg midi=48, speed=3, out=0;
	var env = Env.perc(releaseTime: 0.01);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+96).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.005);
	Out.ar(out, pan);
}).add;

SynthDef(\R, {
	arg midi=48, speed=3, out=0;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(out, pan);
}).add;

SynthDef(\R2, {
	arg midi=48, speed=3, out=0;
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
}, '/s_new');
)