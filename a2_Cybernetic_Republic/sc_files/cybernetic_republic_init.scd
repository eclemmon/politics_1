(
MIDIClient.init;
TempoClock.tempo = 2;


~gm = Dictionary.newFrom(
	[
		\recv_netaddress, NetAddr.new("127.0.0.1", 57120),
		\visuals_netaddress, NetAddr.new("127.0.0.1", 12000),
		\mOuts, Dictionary.newFrom([\rhythm, MIDIOut.new(0), \middle_voice, MIDIOut.new(1)]),
		\break_beat_1, List.new(),
		\middle_voice, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]),
		\rhythm_pattern, nil,
		\middle_voice_pattern, nil,
		\arpeggiator_on, false
	]
);

CmdPeriod.add({
	(0..127).do({arg n; ~gm.at(\mOuts).do({arg out; out.noteOff(0, n)})});
	16.do({arg i; ~gm.at(\mOuts).at(\middle_voice).control(i, 0, 0)});
});

)