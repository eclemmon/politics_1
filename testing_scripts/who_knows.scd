s = Server.default.boot;
Server.default.options.outDevice_("Multi-Output Device");
~netaddress = NetAddr.new("127.0.0.1", 57120)

(
SynthDef(\Q, {
	arg midi=48, speed=3;
	var env = Env.perc;
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+60).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.5);
	Out.ar(0, pan);
}).add;

SynthDef(\L, {
	arg midi=48, speed=0.1;
	var env = Env.new(
		levels: [0,1,0],
		times: [2,3]);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var saw = Saw.ar((midi%12+24).midicps, 2);
	var sin = SinOsc.ar((midi%12+24).midicps, 2);
	var sig = sin * saw * envgen;
	var filter = LPF.ar(sig, 100);
	var pan = Pan2.ar(filter, pos: SinOsc.kr(0.1), level: 1);
	Out.ar(0, pan);
}).add;

SynthDef(\P, {
	arg midi=48, speed=3;
	var env = Env.perc(releaseTime: 0.01);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+96).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.005);
	Out.ar(0, pan);
}).add;

SynthDef(\R, {
	arg midi=48, speed=3;
	var env = Env.perc(0.2);
	var envgen = EnvGen.kr(env, Dust.kr(speed));
	var sin = SinOsc.ar((midi%12+72).midicps, 0.5);
	var sig = sin * envgen;
	var pan = Pan2.ar(sig, pos: SinOsc.kr(2), level: 0.1);
	Out.ar(0, pan);
}).add;
)


(
~q_chord = [48,48,48].collect({
	arg note, index;
	Synth(\Q, [\midi, note, \speed, index*0.3]);
});

~l_chord = [48,48,48].collect({
	arg note, index;
	Synth(\L, [\midi, note, \speed, index*0.2]);
});

~p_chord = [48,48,48].collect({
	arg note, index;
	Synth(\P, [\midi, note, \speed, index*4]);
});

~r_chord = [48,48,48].collect({
	arg note, index;
	Synth(\R, [\midi, note, \speed, index*0.4]);
});

OSCFunc({ |args|
	"OSCFUNC received the following values:".postln;
	args.postln;
	args[2..4].postln;
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