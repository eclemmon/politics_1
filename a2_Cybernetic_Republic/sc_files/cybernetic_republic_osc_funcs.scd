(
OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	// args.postcs;
	~add_durations_to_dict.value(~gm, args[1], Array.fill(args[2..].size, {
		arg i;
		if((args[i+2] == '/r'), {
			Rest(0.25);
		}, {
			args[i+2];
		});
	})
	);

	"######################################".postln;
}, '/message');

OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	// Stop previous pattern
	~gm.at(args[2].asSymbol).stop;
	// Run the pattern
	~gm.put(args[2].asSymbol, ~build_ppar.value(~gm, args[1].asSymbol, args[2].asSymbol));
	~gm.at(args[2].asSymbol).play;
	// Empty the pattern list
	~clear_midinotes_durations_at_key.value(~gm, args[1].asSymbol);
	"######################################".postln;
}, '/init');


OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	// args.postcs;
	~add_midinotes_durations_to_dict.value(~gm, \break_beat_1, Array.fill(args[2..].size, {arg i; args[1]}), Array.fill(args[2..].size, {
		arg i;
		if((args[i+2].asString.beginsWith("/r")), {
			if(args[i+2] == '/r', {
				Rest(0.25);
				0.25.postln;
			}, {
				Rest(args[i+2].asString[2..].asFloat);
				args[i+2].asString[2..].asFloat.postln;
			});
		}, {
			args[i+2];
		});
	})
	);

	"######################################".postln;
}, '/break_beat_1');

// #######################
// MIDDLE VOICES OSC FUNCS
// #######################

OSCFunc({ |args|
	// Clear the middle voices array so that a new pattern can be built
	~clear_middle_voices.value(~gm);
}, '/clear_middle_voice');

OSCFunc({ |args|
	args.postcs;
	// Add chords as they come in to build a 2d array
	~gm.at(\middle_voice).at(\midinotes).add(args[1..]);
}, '/middle_voice_chords');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	args.postcs;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\middle_voice).put(\durations, durations);
}, '/middle_voice_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// build and run the pattern
	~gm.put(\middle_voice_pattern, ~build_pattern.value(~gm, \middle_voice, \middle_voice, channel));
	"MIDDLE VOICES INITIALIZED!".postln;
	~gm.at(\middle_voice_pattern).play;
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
	args.postcs;
	// Add chords as they come in to build a 2d array
	~gm.at(\melody).at(\midinotes).add(args[1]);
}, '/melody_notes');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	args.postcs;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\melody).put(\durations, durations);
}, '/melody_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// build and run the pattern
	~gm.put(\melody_pattern, ~build_pattern.value(~gm, \melody, \melody, channel));
	"MELODY INITIALIZED!".postln;
	~gm.at(\melody_pattern).play;
	~clear_voice.value(~gm, \melody);
}, 'melody_init');

// #######################
// BASS OSC FUNCS
// #######################

OSCFunc({ |args|
	args.postcs;
	// Add chords as they come in to build a 2d array
	~gm.at(\bass).at(\midinotes).add(args[1]);
}, '/bass_notes');

OSCFunc({ |args|
	// Add durations to ~gm.at(\middle_voice_durations). Needs to be a 1d array
	var durations;
	args.postcs;
	durations = ~parse_rests_and_notes.value(args[1..]);
	~gm.at(\bass).put(\durations, durations);
}, '/bass_durations');

OSCFunc({ |args|
	var durations, chords, channel;
	// Get middle voice channel (random instrument selected)
	channel = args[1];
	// build and run the pattern
	~gm.put(\bass_pattern, ~build_pattern.value(~gm, \bass, \bass, channel));
	"BASS INITIALIZED!".postln;
	~gm.at(\bass_pattern).play;
	~clear_voice.value(~gm, \bass);
}, 'bass_init');

)

~gm.at(\mOuts).at(\middle_voice).control(15, 0, 0)
~gm.at(\melody);
~gm.at(\middle_voice_pattern).postcs
~gm.at('rhythm').stop;
~gm.at('arpeggiator_on');
