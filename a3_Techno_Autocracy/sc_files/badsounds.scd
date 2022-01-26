s = Server.default.boot;
Server.default.options.outDevice_("Multi-Output Device");
(
SynthDef.new(\low_hum, {
	arg out, amp, time_to_return, filter_freq;
	var noise, rand_amp, filter;
	noise = ClipNoise.ar(1);
	rand_amp = LFNoise0.kr(0.5 + LFNoise0.kr(10).range(-0.1, 0.5));
	filter = RLPF.ar(noise*rand_amp, filter_freq, rq: 0.001, mul: amp);
	Out.ar(out, [filter, filter]);
}).add;
)


(
SynthDef.new(\high_hum, {
	arg out, amp, time_to_return, filter_freq;
	var clipper, rand_amp;
	clipper = Clip.ar(SinOsc.ar(500)*SinOsc.ar(1824)*Saw.ar(87), -0.2, 0.2);
	rand_amp = LFNoise0.kr(0.01).range(0.5, 0.8);
	Out.ar(out, [clipper*rand_amp, clipper*rand_amp]);
}).add;
)




(
~low_hum_group = Group.new;
Array.fill(10, {arg i; Synth(\low_hum, [\out, 0, \amp, 1, \filter_freq, i*10+40], ~low_hum_group, \addToHead)});
)

(
~low_hum_group.set(\amp, 1.0);
Synth(\high_hum, [\out, 0, \amp, 0.9, \filter_freq, 30]);
Synth(\high_hum, [\out, 0, \amp, 0.9, \filter_freq, 70]);
)

Synth(\high_hum, [\out, 0, \amp, 0.9, \filter_freq, 6000]);