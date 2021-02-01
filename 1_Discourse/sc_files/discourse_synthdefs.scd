

(
// NEW SYNTH DEFS FOR PSEQ
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