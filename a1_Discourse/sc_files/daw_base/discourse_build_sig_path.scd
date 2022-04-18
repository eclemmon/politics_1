(
// #####################################################################################################################
// discourse_build_sig_path.scd
// ---------------------------------------------------------------------------------------------------------------------
// This function parses incoming data from python and sends it out to Live.
// #####################################################################################################################

~buildSignalPath = {
    // Function that builds the signal path to pass over to Live.
	arg vals, mem;
	var total_dur, dvals, rvals, spatvals, dt, dd, predelay, reverbtime, lpf, mix, start_point, target, time_interval, instruments, patterns, octave, rhythm, sus_vals, mod_vals, modAmp, modFreq, mOut, panRoutine, panRoutines, panChannel;
	// Get MidiOut
	mOut = mem.at(\mOut).at(mem.at(\mOutIndex));

    // Functions to parse incoming arguments.
	total_dur = ~get_total_dur_value.value(vals);
	dvals = ~get_delay_values.value(vals);
	rvals = ~get_reverb_values.value(vals);
	spatvals = ~get_spat_values.value(vals);
	instruments = ~get_instrument_names.value(vals);
	octave = ~get_octave_value.value(vals);
	rhythm = ~get_rhythm_data.value(vals);
	sus_vals = ~build_sus_data.value(rhythm, total_dur);
	mod_vals = ~get_mod_values.value(vals);

	// Delay values
	dt = dvals[0];
	dd = dvals[1];

	// Reverb Values
	predelay = rvals[0];
	reverbtime = rvals[1];
	lpf = rvals[2];
	mix = rvals[3];

	// Spatialization Values
	time_interval = spatvals[0];
	start_point = spatvals[1];
	target = spatvals[2];

	// Freq Mod values
	modAmp = mod_vals[0];
	modFreq = mod_vals[1];


	~print_vals.value([total_dur, dvals, rvals, spatvals, instruments, time_interval, total_dur, octave, rhythm, sus_vals]).postln;
	// Stop pan Routines at current mOutIndex
	"MOutIndex:".postln;
	mem.at(\mOutIndex).postln;
	mem.at(\panRoutines).at(mem.at(\mOutIndex)).stop;

	// Set control values
	instruments.do({
		arg item;
		var channel = mem.at(\channels).at(item);
		~controlDelayTime.value(mOut, channel, dt);
		~controlDelayFeedback.value(mOut, channel, dd);
		~controlReverbPredelay.value(mOut, channel, predelay);
		~controlReverbDecayTime.value(mOut, channel, reverbtime);
		~controlReverbLPFGain.value(mOut, channel, lpf);
		~controlReverbDryWet.value(mOut, channel, mix);
		~controlModFreq.value(mOut, channel, modFreq);
		~controlModAmp.value(mOut, channel, modAmp);
		// make pan routine for the instrument
	});

	// get pan Channel
	panChannel = mem.at(\panChannels).at(mem.at(\mOutIndex));
	"panChannel".postln;
	panChannel.postln;

	// Create panRoutine
	panRoutine = ~controlPan.value(mem.at(\mOut).at(0), panChannel, start_point, target, time_interval);

	// Play pan routine
	panRoutine.play;

	// Add Pan Routine to storage
	mem.at(\panRoutines).put(mem.at(\mOutIndex), panRoutine);

	// Create midi pattern
	patterns = Array.fill(instruments.size, {arg i; ~createMidiPattern.value(vals, mOut, instruments[i])} );
	Ppar(patterns).play;

	// Update MidiOut index
	mem.put(\mOutIndex, ((mem.at(\mOutIndex) + 1) % mem.at(\mOut).size));
};
)


