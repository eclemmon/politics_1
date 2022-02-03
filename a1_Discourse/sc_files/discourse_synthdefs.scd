(
// H/t Eli Fieldsteel
SynthDef(\reverb, {
	arg in, predelay=1, revtime=10, lpf=4500, mix=0.5, amp=1, out=0, dur=1, gate=1, doneAction=2, time_interval=4, start_point=(-1), target=1;
	var dry, wet, temp, sig, env, pan, leakDC;
	dry = In.ar(in, 2);
	temp = In.ar(in, 2);
	wet = 0;
	temp = DelayN.ar(temp, revtime, predelay);
	4.do({
		temp = AllpassN.ar(temp, 0.05, {Rand(0.001, 0.05)}!2, revtime);
		temp = LPF.ar(temp, lpf);
		wet = wet + temp;
	});
	env = EnvGen.kr(Env([0,1,1,0], [0.05, dur+1, 0.1], curve: (-2)), gate, doneAction: doneAction);
	sig = XFade2.ar(dry, wet, mix * 2 - 1, amp) * env;
	pan = Pan2.ar(sig.dup, Line.kr(start_point, target, time_interval));
	Out.ar(out, pan);
}).add;

SynthDef(\linear_spat_motion, {
	arg in, time_interval=1, start_point, target, amp=1, out=0, dur=1, gate=0;
	var input, lin_motion, sig, env;
	input = In.ar(in, 2);
	env = EnvGen.kr(Env([0,1,1,0], [0.05, dur, 0.1], curve: (-2)), gate, doneAction: 2);
	lin_motion = Pan2.ar(input, Line.kr(start_point, target, time_interval));
	sig = lin_motion * amp * env;
	Out.ar(out, sig);
}).add;

SynthDef(\delay, {
	arg in, out=0, max_delay=0.2, delaytime=0.2, decaytime=1.0, amp=1, dur, gate=1;
	var input, delay, sig, env, leakDC;
	input = In.ar(in, 2);
	env = EnvGen.kr(Env([0,1,1,0], [0.05, dur, 0.1], curve: (-2)), gate, doneAction: 2);
	delay = CombN.ar(input, max_delay, delaytime, decaytime);
	sig = delay * amp * env;
	leakDC = LeakDC.ar(sig);
	Out.ar(out, leakDC.dup);
}).add;

SynthDef(\sin, {
	arg freq=440, out=0, mFreq, mAmp, dur, gate=1, amp=0.5;
	var env, sig, detuneSig;
	env = EnvGen.kr(Env([0, 1, 0.1, 0], [0.01, dur, 0.1], curve: [-2, -2, 'lin'], releaseNode: 1), gate, doneAction: 2);
	sig = SinOsc.ar(freq, SinOsc.kr(mFreq, mul: mAmp)) * amp * env;
	Out.ar(out, sig);
}).add;

SynthDef(\saw, {
	arg freq=440, out=0, mFreq, mAmp, dur=1, gate=1, amp=0.5;
	var env, sig, mod, detuneSig;
	env = EnvGen.kr(Env.adsr(releaseTime: 0.2), gate, doneAction: 2);
	mod = LFTri.kr(LFNoise1.kr(2)).range(0, 1);
	sig = VarSaw.ar(LFSaw.kr(mFreq, 0, 0.2, freq, mAmp * 2), 0, mod) * env * amp;
	Out.ar(out, sig);
}).add;

SynthDef(\noise, {
	arg freq=440, out=0, gate=1, amp=0.5, dur=1, mFreq, mAmp;
	var env, sig;
	env = EnvGen.kr(Env.adsr(releaseTime: 0.2), gate, doneAction: 2);
	sig = Dust2.ar(freq * LFNoise1.kr(mFreq, mAmp), LFNoise1.kr(mFreq)) * env;
	Out.ar(out, sig);
}).add;

SynthDef(\impulse, {
	arg freq=440, out=0, gate=1, amp=0.5, dur=1, mFreq, mAmp;
	var env, sig;
	env = EnvGen.kr(Env([0, 1, 0.4, 0], [0.01, dur, 0.1], curve: [-2, -2, 'lin'], releaseNode: 1), gate, doneAction: 2);
	sig = Impulse.ar(freq, LFNoise1.kr(mFreq, mul: mAmp)) * amp * env;
	Out.ar(out, sig);
}).add;

SynthDef(\square, {
	arg freq=440, out=0, mFreq, mAmp, dur=1, gate=1, amp=0.5;
	var env, sig;
		env = EnvGen.kr(Env([0, 1, 0.1, 0], [0.01, dur, 0.1], curve: [-2, -2, 'lin'], releaseNode: 1), gate, doneAction: 2);
	sig = Pulse.ar(freq, LFNoise1.kr(mFreq, mul: mAmp)) * amp * env;
	Out.ar(out, sig);
}).add;

SynthDef(\wavetable, {
	arg out=0, buf=0, numBufs=2, freq=300, amp=1, gate=1, dur=1, mFreq, mAmp;
	var sig, bufpos, detuneSig, panning, leakDC, env;
	env = EnvGen.kr(Env([0, 1, 0.1, 0], [0.01, dur, 0.1], curve: [-2, -2, 'lin'], releaseNode: 1), gate, doneAction: 2);
	bufpos = buf + LFNoise1.kr(0.5).range(0, numBufs-1);
	sig = VOsc.ar(bufpos, freq);
	panning = Splay.ar(sig);
	leakDC = LeakDC.ar(panning) * amp * env;
	Out.ar(out, leakDC);
}).add;

SynthDef.new(\soundInRouter, {
	// Routes one input bus to an output, also allows for amplitude control.
	arg in=0, out=0, amp=1;
	var sig;
	sig = SoundIn.ar(in) * amp;
	Out.ar(out, sig);
}).add;

SynthDef.new(\pointer, {
	// A pointer, written to a bus that 'trails' the realtime "head" of an audio bus.
	arg out=0, buf=0;
	var sig;
	sig = Phasor.ar(0, BufRateScale.kr(buf), 0, BufFrames.kr(buf));
	Out.ar(out, sig);
}).add;

SynthDef.new(\recordBuffer, {
	// Records a signal into a buffer from the pointer's position.
	arg ptrIn=0, recIn=0, buf=0;
	var ptr, sig;
	ptr = In.ar(ptrIn, 1);
	sig = In.ar(recIn, 1);
	BufWr.ar(sig, buf, ptr);
}).add;

SynthDef.new(\splitter, {
	// A helper audio bus splitter to send one audio inout to two audio buses out.
	arg in=10, out1=89, out2=99, dur, gate=1;
	var input, env;
	env = EnvGen.kr(Env([0,1,1,0], [0.05, dur, 0.1], curve: [-2, -2, 'lin'], releaseNode: 1), gate, doneAction: 2);
	input = In.ar(in, 2);
	Out.ar([out1, out2], input);
}).add;

SynthDef.new(\granulator, {
	// Granulator.
	arg amp=1, out=0, buf=0, attack=1, sustain=1, release=1, gate=1, sync=0, density=40, baseDur=0.05, durRand=1, rate=1, rateRand=1, pan=0, panRand=1, grainEnv=(-1), ptrBus=0, ptrSampleDelay=20000, ptrRandSamples=5000, minPtrDelay=1000;
	var sig, env, densCtrl, durCtrl, rateCtrl, panCtrl, ptr, ptrRand, totalDelay, maxGrainDur, grain;

	env = EnvGen.kr(Env.asr(attack, sustain, release), gate, doneAction:2);
	densCtrl = Select.ar(sync, [Dust.ar(density), Impulse.ar(density)]);
	durCtrl = baseDur * LFNoise1.ar(100).exprange(1/durRand, durRand);
	rateCtrl = rate * LFNoise1.ar(100).exprange(1/rateRand, rateRand);
	panCtrl = pan + LFNoise1.kr(100).bipolar(panRand);

	ptrRand = LFNoise1.ar(100).bipolar(ptrRandSamples);
	totalDelay = max(ptrSampleDelay - ptrRand, minPtrDelay);

	ptr = In.ar(ptrBus, 1);
	ptr = ptr - totalDelay;
	ptr = ptr / BufFrames.kr(buf);

	maxGrainDur = (totalDelay / rateCtrl) /SampleRate.ir;
	durCtrl = min(durCtrl, maxGrainDur);

	grain = GrainBuf.ar(
		2,
		densCtrl,
		durCtrl,
		buf,
		rateCtrl,
		ptr,
		2,
		panCtrl,
		grainEnv
	);

	sig = grain * env * amp;
	Out.ar(out, sig);
}).add;
)