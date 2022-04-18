(
// #####################################################################################################################
// cybernetic_republic_init.scd
// ---------------------------------------------------------------------------------------------------------------------
// This file initializes some bass logic and containers in memory for storing data coming in from python for later,
// concurrent initialization.
// #####################################################################################################################

// Initialize MIDIClient
MIDIClient.init;

// Set TempoClock to 120 BPM for some pop.
TempoClock.tempo = 2;

// Initialize global memory
~gm = Dictionary.newFrom(
	[
		\recv_netaddress, NetAddr.new("127.0.0.1", 57120),
		\visuals_netaddress, NetAddr.new("127.0.0.1", 12000),
		\mOuts, Dictionary.newFrom([\rhythm_section, MIDIOut.new(0), \middle_voice, MIDIOut.new(1), \bass, MIDIOut.new(2), \melody, MIDIOut.new(3)]),
		\rhythm_section, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]),
		\middle_voice, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]),
		\melody, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]),
		\bass, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]),
		\rhythm_pattern, nil,
		\middle_voice_pattern, nil,
		\bass_pattern, nil,
		\melody_pattern, nil,
		\arpeggiator_on, false,
		\quantization, 16
	]
);

// Add command to turn all midi notes off on CmdPeriod.
CmdPeriod.add({
	(0..127).do({arg n; ~gm.at(\mOuts).do({arg out; out.noteOff(0, n)})});
	16.do({arg i; ~gm.at(\mOuts).at(\middle_voice).control(i, 0, 0)});
});

)