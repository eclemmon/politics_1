(

// #######################
// RHYTHM OSC FUNCS
// #######################

OSCFunc({ |args|
	// Stop previous pattern
	// ~gm.at(\rhythm_pattern).stop;
	// Run the pattern
	~gm.put(\rhythm_pattern, ~build_ppar.value(~gm, \rhythm_section, \rhythm_section));
	~gm.at(\rhythm_pattern).play(quant: ~gm.at(\quantization));
	"RHYTHM INITIALIZED!".postln;
	// Empty the pattern list
	~clear_voice.value(~gm, \rhythm_section);
}, '/rhythm_init');


OSCFunc({ |args|
	~gm.at(\rhythm_section).at(\midinotes).add(Array.fill(args[2..].size, {arg i; args[1]}));
	~gm.at(\rhythm_section).at(\durations).add(~parse_rests_and_notes.value(args[2..]));
}, '/rhythm_section');

// #######################
// MIDDLE VOICES OSC FUNCS
// #######################

OSCFunc({ |args|
	// Clear the middle voices array so that a new pattern can be built
	~clear_middle_voices.value(~gm);
}, '/clear_middle_voice');

OSCFunc({ |args|
	// Add chords as they come in to build a 2d array
	~gm.at(\middle_voice).at(\midinotes).add(args[1..]);
}, '/middle_voice_chords');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\middle_voice).put(\durations, durations);
}, '/middle_voice_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// ~gm.at(\middle_voice_pattern).stop;
	// build and run the pattern
	~gm.put(\middle_voice_pattern, ~build_pattern.value(~gm, \middle_voice, \middle_voice, channel));
	"MIDDLE VOICES INITIALIZED!".postln;
	~gm.at(\middle_voice_pattern).play(quant: ~gm.at(\quantization));
	~clear_voice.value(~gm, \middle_voice);
}, 'middle_voice_init');

OSCFunc({ |args|
	if(~gm.at(\arpeggiator_on) == true, {
		// Turn off Arpeggiator
		"Turning Arpeggiator off".postln;
		16.do({arg i; ~gm.at(\mOuts).at(\middle_voice).control(i, 0, 0)});
		// Set \arpeggiator_on to false
		~gm.put(\arpeggiator_on, false);
	}, {
		// Turn on Arpeggiator
		"Turning Arpeggiator On".postln;
		16.do({arg i; ~gm.at(\mOuts).at(\middle_voice).control(i, 0, 127)});
		~gm.put(\arpeggiator_on, true);
	});
}, '/arpeggiator');

// #######################
// MELODY OSC FUNCS
// #######################

OSCFunc({ |args|
	// Add chords as they come in to build a 2d array
	~gm.at(\melody).at(\midinotes).add(args[1]);
}, '/melody_notes');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\melody).put(\durations, durations);
}, '/melody_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// Stop the pattern
	// ~gm.at(\melody_pattern).stop;
	// build and run the pattern
	~gm.put(\melody_pattern, ~build_pattern.value(~gm, \melody, \melody, channel));
	"MELODY INITIALIZED!".postln;
	~gm.at(\melody_pattern).play(quant: ~gm.at(\quantization));
	~clear_voice.value(~gm, \melody);
}, 'melody_init');

// #######################
// BASS OSC FUNCS
// #######################

OSCFunc({ |args|
	// Add chords as they come in to build a 2d array
	~gm.at(\bass).at(\midinotes).add(args[1]);
}, '/bass_notes');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\bass).put(\durations, durations);
}, '/bass_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// ~gm.at(\bass_pattern).stop;
	// build and run the pattern
	~gm.put(\bass_pattern, ~build_pattern.value(~gm, \bass, \bass, channel));
	"BASS INITIALIZED!".postln;
	~gm.at(\bass_pattern).play(quant: ~gm.at(\quantization));
	~clear_voice.value(~gm, \bass);
}, 'bass_init');


// #######################
// OTHER OSC FUNCS
// #######################

OSCFunc({ |args|
	// Put new quantization in the dictionary.
	// Should always be the last call in the OSC sends since the "next bar" should be a downbeat, and not the middle of preceding meter.
	~gm.put(\quantization, args[1]);
	"########## ALL TASKS INITIALIZED #########".postln;
}, '/quantization');
)