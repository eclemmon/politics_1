(
// #####################################################################################################################
// discourse_pattern_builders.scd
// ---------------------------------------------------------------------------------------------------------------------
// A set of functions that build SC Patterns based on input data.
// #####################################################################################################################

~build_saw_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \saw,
		\sustain, Pseq(sus_vals, 1),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(0.7, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 5, 10),
		\mFreq, modvals[1].linlin(0, 30, 5, 10),
		\group, group
	);
	pattern;
};

~build_sin_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \sin,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(0.9, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_noise_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \noise,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\amp, Pgauss(8, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 20, 40),
		\mFreq, modvals[1].linlin(0, 30, 20, 40),
		\group, group
	);
	pattern;
};


~build_impulse_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \impulse,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(5, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_square_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \square,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(0.7, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group
	);
	pattern;
};

~build_wavetable_pattern = {
	arg array, group, outbus, bufs;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \wavetable,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.7, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 2, 40),
		\mFreq, modvals[1].linlin(0, 30, 2, 40),
		\group, group,
		\numBufs, bufs.size,
		\buf, bufs[0].bufnum
	);
	pattern;
};

~build_peep_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \peep,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave + 1,
		\amp, Pgauss(0.7, 0.1, inf),
		\mAmp, modvals[0].linlin(0, 30, 0, 10),
		\mFreq, modvals[1].linlin(0, 30, 0, 10),
		\group, group
	);
	pattern;
};

~build_subtract_pattern = {
	arg array, group, outbus;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);

	pattern = Pbind(
		\instrument, \subtract,
		\sustain, Pseq(sus_vals, 1), //(total_dur / array.size),
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, outbus.index,
		\note, ~build_notes_Pwrand.value(chords_data),
		\octave, octave,
		\amp, Pgauss(0.5, 0.01, inf),
		\mAmp, modvals[0].linlin(0, 30, 1, 30),
		\mFreq, modvals[1].linlin(0, 30, 1, 30),
		\group, group
	);
	pattern;
};

~build_grain_pattern = {
	arg array, group, outbus, memory;
	var pattern, modvals, octave, total_dur, chords_data, rhythm_data, sus_vals, buffer;
	// Get input data
	modvals = ~get_mod_values.value(array);
	octave = ~get_octave_value.value(array);
	total_dur = ~get_total_dur_value.value(array);
	chords_data = ~get_chords_data.value(array);
	rhythm_data = ~get_rhythm_data.value(array);
	sus_vals = ~build_sus_data.value(rhythm_data, total_dur);
	buffer = memory.at(\granBuffer);

	pattern = Pbind(
		\instrument, \granulator,
		\dur, ~build_dur_Pseq.value(rhythm_data, total_dur),
		\out, 0,
		\buf, buffer.bufnum,
		\amp, Pgauss(1, 0.01, inf),
		\rateRand, modvals[0].linlin(0, 30, 0.1, 1),
		\ptrRandSamples, modvals[1].linlin(0, 30, 1000, 10000),
		\group, group,
		\ptrBus, memory.at(\ptrBus);
	);
	pattern;
};
)
