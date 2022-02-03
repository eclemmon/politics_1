// Pattern Builders
(
~build_saw_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \saw,
		\sustain, (total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_sin_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \sin,
		\sustain, (total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_noise_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \noise,
		\sustain, (total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};


~build_impulse_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \impulse,
		\sustain, (total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_square_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \square,
		\sustain, (total_dur / array.size) * 2,
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_wavetable_pattern = {
	arg array, group, outbus, bufs;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);

	pattern = Pbind(
		\instrument, \wavetable,
		\sustain, (total_dur / array.size) * 2,
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.3, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group,
		\numBufs, bufs.size,
		\buf, bufs[0].bufnum
	);
	pattern;
};

)