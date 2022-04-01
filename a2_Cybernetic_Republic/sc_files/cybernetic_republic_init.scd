(
MIDIClient.init;
TempoClock.tempo = 2;
~gm = Dictionary.newFrom(
	[
		\recv_netaddress, NetAddr.new("127.0.0.1", 57120),
		\visuals_netaddress, NetAddr.new("127.0.0.1", 12000),
		\break_beat_1, List.new(),
		\mOuts, Dictionary.newFrom([\rhythm, MIDIOut.new(0)]),
		\rhythm, nil
	]
)

)