s = Server.default.boot;

~netaddress = NetAddr.new("127.0.0.1", 57120)

(
SynthDef(\Q, {
	arg midi = #[0,0,0];
	var midi_res = Array.fill( 3,{ arg i; midi[i]} );
	var sig1 = SinOsc.ar(midi_res[0].midicps, 0.5);
	var sig2 = SinOsc.ar(midi_res[1].midicps, 0.5);
	var sig3 = SinOsc.ar(midi_res[2].midicps, 0.5);
	var sig = sig1 * sig2 * sig3;
	Out.ar(0, [sig, sig]);
}).add;

SynthDef(\L, {
	arg midi = #[0,0,0];
	var midi_res = Array.fill( 3,{ arg i; midi[i]} );
	var sig1 = SinOsc.ar(midi_res[0].midicps, 0.5);
	var sig2 = SinOsc.ar(midi_res[1].midicps, 0.5);
	var sig3 = SinOsc.ar(midi_res[2].midicps, 0.5);
	var sig = sig1 * sig2 * sig3;
	Out.ar(0, [sig, sig]);
}).add;

SynthDef(\P, {
	arg midi = #[0,0,0];
	var midi_res = Array.fill( 3,{ arg i; midi[i]} );
	var sig1 = SinOsc.ar(midi_res[0].midicps, 0.5);
	var sig2 = SinOsc.ar(midi_res[1].midicps, 0.5);
	var sig3 = SinOsc.ar(midi_res[2].midicps, 0.5);
	var sig = sig1 * sig2 * sig3;
	Out.ar(0, [sig, sig]);
}).add;

SynthDef(\R, {
	arg midi = #[0,0,0];
	var midi_res = Array.fill( 3,{ arg i; midi[i]} );
	var sig1 = SinOsc.ar(midi_res[0].midicps, 0.5);
	var sig2 = SinOsc.ar(midi_res[1].midicps, 0.5);
	var sig3 = SinOsc.ar(midi_res[2].midicps, 0.5);
	var sig = sig1 * sig2 * sig3;
	Out.ar(0, [sig, sig]);
}).add;
)


(
q = Synth(\Q, [\midi, [48,48,48]]);
l = Synth(\L, [\midi, [48,48,48]]);
p = Synth(\P, [\midi, [48,48,48]]);
r = Synth(\R, [\midi, [48,48,48]]);
// ~sinTone = Synth(\sinTone, [\freq,1000]);

OSCFunc({ |args|
	"OSCFUNC received the following values:".postln;
	args.postln;
	args[2..4].postln;
	q.set(\midi, args[2..4]);
	l.set(\midi, args[6..8]);
	p.set(\midi, args[10..12]);
	r.set(\midi, args[14..16]);
}, '/s_new');
)