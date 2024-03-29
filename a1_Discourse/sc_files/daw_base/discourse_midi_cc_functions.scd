// #####################################################################################################################
// discourse_midi_cc_functions.scd
// ---------------------------------------------------------------------------------------------------------------------
// A group of MIDI functions to control Live via midi.
// All functions control Live by sending out to a particular MIDI out bus on Mac's internal IAC driver, and a midi
// channel on the bus. Most functions are self explanatory by their name. Additional documentation is added where
// needed.
// #####################################################################################################################
(
~controlDelayTime = {
	arg midiOut, channel, value;
	midiOut.control(channel, 0, value.linlin(0.1, 5, 0, 127));
};

~controlDelayFeedback = {
	arg midiOut, channel, value;
	midiOut.control(channel, 1, value.linlin(0.1, 5, 0, 127));
};

~controlReverbPredelay = {
	arg midiOut, channel, value;
	midiOut.control(channel, 2, value.linlin(0, 1, 0, 127));
};

~controlReverbDecayTime = {
	arg midiOut, channel, value;
	midiOut.control(channel, 3, value.linlin(0, 1, 0, 127));
};

~controlReverbLPFGain = {
	arg midiOut, channel, value;
	midiOut.control(channel, 4, value.linlin(0, 1, 0, 127));
};

~controlReverbDryWet = {
	arg midiOut, channel, value;
	midiOut.control(channel, 5, value.linlin(0, 1, 0, 127));
};

~controlPan = {
    // #################################################################################################################
    // ~controlPan
    // -----------------------------------------------------------------------------------------------------------------
    // Mimicking a Line function in Max or Supercollider, this function spins off a routine when triggered to control
    // the MIDI values of an instrument's pan over a given time span.
    // #################################################################################################################
	arg midiOut, channel, startVal, endVal, time;
	var routine, increment, distance, waitTime, currentVal;
	distance = abs(endVal.linlin(-1, 1, 0, 127) - startVal.linlin(-1, 1, 0, 127));
	waitTime = time / distance;
	currentVal = startVal.linlin(-1, 1, 0, 127);
	if(startVal >= endVal, {
		increment = -1;
	}, {
		increment = 1;
	});
	routine = Routine.new({
		if (increment > 0, {
			forBy(currentVal, endVal.linlin(-1, 1, 0, 127), increment, {
				currentVal = currentVal + increment;
				if(currentVal > 127, {currentVal = 127});
				midiOut.control(0, channel, currentVal);
				waitTime.wait;
			});
		}, {
			forBy(currentVal, endVal.linlin(-1, 1, 0, 127), increment, {
				currentVal = currentVal + increment;
				if(currentVal < 0, {currentVal = 0});
				midiOut.control(0, channel, currentVal);
				waitTime.wait;
			});

		});
	});
	routine;
};

~controlModFreq = {
	arg midiOut, channel, value;
	midiOut.control(channel, 7, value.linlin(0, 30, 0, 127));
};

~controlModAmp = {
	arg midiOut, channel, value;
	midiOut.control(channel, 8, value.linlin(0, 30, 0, 127));
};

~createMidiPattern = {
	arg array, mOut, channel;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

    // Build the pattern
	pattern = Pbind(
		\type, \midi,
		\midicmd, \noteOn,
		\midiout, mOut,
		\chan, channel,
		\sustain, Pseq(sus_vals, array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\degree, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(0.9, 0.1, inf),
	);
	pattern;
};


)
