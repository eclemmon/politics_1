s = Server.default.boot;
Server.default.options.outDevice_("Multi-Output Device");
~netaddress = NetAddr.new("127.0.0.1", 57120)

(
// OSC FUNC WITH Pseq?
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