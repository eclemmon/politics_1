(
SynthDef.new(\bitCrush, {
	arg out=0, maxFreqAdd=1000, minFreq=(SampleRate.ir * 0.25), x0=0.1, y0=2.1, amp=1, gate=1, dur=10, pos=0;
	var minFreqRand, maxFreqRand, env, sig, splay, bitCrush, sin, mix, pan;
	env = EnvGen.kr(Env.adsr(releaseTime: 0.1), gate: gate, doneAction: 2);
	minFreqRand = LFNoise1.kr(30, minFreq+20, 20);
	maxFreqRand = minFreqRand + LFNoise1.kr(20, maxFreqAdd, maxFreqAdd);
	bitCrush = Gbman2DN.ar(minFreqRand, maxFreqRand, x0, y0) * env * VarLag.kr(amp, 0.01);
	pan = Pan2.ar(bitCrush, pos);
	Out.ar(out, pan)
}).add;

SynthDef.new(\lowClip, {
	arg out, amp=1, filter_freq, gate=1, dur=10, pos=0;
	var noise, rand_amp, filter, env, pan;
	noise = ClipNoise.ar(1);
	env = EnvGen.kr(Env.adsr(releaseTime: 0.1), gate: gate, doneAction: 2);
	rand_amp = LFNoise1.kr(0.5 + LFNoise1.kr(10).range(-0.1, 0.5));
	filter = RLPF.ar(noise*rand_amp, filter_freq, rq: 0.001, mul: amp) * env;
	pan = Pan2.ar(filter, pos);
	Out.ar(out, pan);
}).add;

SynthDef.new(\standardNNoise, {
	arg out=0, amp=1, octave=1, unhook=0, gate=1, pos=0;
	var sig, env, select, pan;
	select = Select.kr(unhook, [0, 1, 2]);
	env = EnvGen.kr(Env.adsr(releaseTime: 0.1), gate: gate, doneAction: 2);
	sig = StandardN.ar(SampleRate.ir/octave, (LFNoise1.kr(3, mul: 0.75, add: 1.5) + select)).dup * 0.3 * env * amp;
	pan = Pan2.ar(sig, pos);
	Out.ar(out, pan);
}).add;

SynthDef.new(\sin, {
	arg out=0, amp=1, freq=440, sinLFOFreq=0.1, lfoPhase=0, pos=0, gate=1;
	var env, sin, pan;
	env = EnvGen.kr(Env.adsr, gate: gate, doneAction: 2);
	sin = SinOsc.ar(VarLag.kr(freq, (60*5), warp: \exp), mul: SinOsc.kr(sinLFOFreq, phase: lfoPhase, mul: 0.5, add: 0.6)) * VarLag.kr(amp, 10, warp: \lin) * env;
	pan = Pan2.ar(sin, pos);
	Out.ar(out, pan);
}).add;

SynthDef.new(\gendy, {
	arg out=0, amp=1, gate=1, pos=0, minFreq=440, maxFreq=660;
	var env, gendy, pan;
	env = EnvGen.kr(Env.adsr, gate: gate, doneAction: 2);
	gendy = Gendy5.ar(minfreq: minFreq, maxfreq: maxFreq) * amp;
	pan = Pan2.ar(gendy, pos);
	Out.ar(out, pan);
}).add;
)



