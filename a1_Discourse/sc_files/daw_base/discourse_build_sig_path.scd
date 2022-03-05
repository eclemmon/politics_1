(
~buildSignalPath = {
	arg vals, mOut;
	var reverb, spat, delay, synths, group, pattern, total_dur, dvals, rvals, spatvals, dt, dd, predelay, reverbtime, lpf, mix, start_point, target, time_interval, instruments, patterns, splitter, sbus, rbus, dbus, fbus, spatbus, octave, filter, rhythm, sus_vals, mod_vals, modAmp, modFreq;
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

	// Set control values
	~controlDelayTime.value(mOut, 0, dt);
	~controlDelayFeedback.value(mOut, 0, dd);
	~controlReverbPredelay.value(mOut, 0, predelay);
	~controlReverbDecayTime.value(mOut, 0, reverbtime);
	~controlReverbLPFGain.value(mOut, 0, lpf);
	~controlReverbDryWet.value(mOut, 0, mix);
	~controlModFreq.value(mOut, 0, modFreq);
	~controlModAmp.value(mOut, 0, modAmp);

	// Create midi pattern
	pattern = ~createMidiPattern.value(vals, mOut);
	pattern.play;

	// Spin pan motion routine off
	~controlPan.value(m, 0, start_point, target, time_interval);

};
)

~buildSignalPath.value(['sound_triggers', 1, 2, 0.0, 0.9383333325386, 0.061666667461395, 0.1203999966383, 6.5357141494751, 0.1203999966383, 0.0, 0.0, 0.0, 2, 3, 4, 'wavetable1', 'wavetable1', 'wavetable1', 'wavetable1', 0.6691871881485, 3.0, 0.0, 3.0, 7.0, 0.49402922391891, 3.0, 0.0, 4.0, 9.0, 0.83678364753723, 3.0, 0.0, 5.0, 8.0, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5], ~mOut);