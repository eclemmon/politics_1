(
~buildWaveTables = {
	arg numTables=4, tableSize=1024;
	var array;
	array = Array.fill(numTables, {
		var numSegs = rrand(4, 20);
		Env(
			levels: [0] ++ (({rrand(0.0, 1.0)}!(numSegs-1)) * [1, -1]).scramble ++ [0],
			times: {exprand(1, 20)}!numSegs,
			curve: {rrand(-20,20)}!numSegs
		).asSignal(tableSize).asWavetable;
	});
	array;
};

~allocConsecutiveBuffers = {
	arg numBuffers, bufSize;
	var buffers;
	buffers = Buffer.allocConsecutive(numBuffers, s, bufSize);
	buffers;
};

~loadWaveTablesToBuffers = {
	arg buffers, waveTables;
	buffers.do({
		arg buf, i;
		buf.loadCollection(waveTables[i]);
	});
	buffers;
};

~makeWtBuffers = {
	arg numBuffers=4, tableSize=1024;
	var waveTables, buffers;
	waveTables = ~buildWaveTables.value(numBuffers, tableSize);
	buffers = ~allocConsecutiveBuffers.value(numBuffers, tableSize*2);
	buffers = ~loadWaveTablesToBuffers.value(buffers, waveTables);
	buffers;
};

~buildGranulatorBuffer = {
	arg server, buffer_size;
	var buffer;
	buffer = Buffer.alloc(server, server.sampleRate * buffer_size);
	buffer;
};

~buildSignalPath.value([ 'sound_triggers', 15, 8, 0.0, 0.9383333325386, 0.061666667461395, 0.1203999966383, 6.5357141494751, 0.1203999966383, 0.0, 0.0, 0.0, 4, 10, 4, 'square', 'sin', 'impulse', 'sin', 0.6691871881485, 3.0, 0.0, 3.0, 7.0, 0.49402922391891, 3.0, 0.0, 4.0, 9.0, 0.83678364753723, 3.0, 0.0, 5.0, 8.0, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5 ]);

~gm = Dictionary.new();
~gm.put('square', ~build_square_pattern);
~gm.put('sin', ~build_sin_pattern);
~gm.put('impulse', ~build_impulse_pattern);

~buildSignalPath = {
	arg vals;
	var reverb, spat, delay, synths, group, rbus, dbus, pattern, events, total_dur, dvals, rvals, spatvals, dt, dd, predelay, reverbtime, lpf, mix, start_point, target, time_interval, instruments;
	total_dur = ~get_total_dur_value.value(vals);
	dvals = ~get_delay_values.value(vals);
	rvals = ~get_reverb_values.value(vals);
	spatvals = ~get_spat_values.value(vals);
	instruments = ~get_instrument_names.value(vals);

	// Delay values
	dt = dvals[0].linlin(0, 30, 0.1, (total_dur / 2));
	dd = dvals[1].linlin(0, 30, 0.1, (total_dur / 2));

	// Reverb Values
	predelay = rvals[0].linlin(0, 1, 1, 3);
	reverbtime = rvals[1].linlin(0, 1, 0, 10);
	lpf = rvals[2].linlin(0, 1, 1000, 6000);
	mix = rvals[3].linlin(-1, 1, 0, 1);

	// Spatialization Values
	time_interval = spatvals[0].linlin(0, 280, (total_dur / 2), total_dur);
	start_point = spatvals[1];
	target = spatvals[2];

	// Automatically allocate buses
	rbus = Bus.audio(s, numChannels: 2);
	dbus = Bus.audio(s, numChannels: 2);

	// Synths
	group = Group.new;
	reverb = Synth(\reverb, [\in, rbus, \predelay, predelay, \revtime, reverbtime, \lpf, lpf, \mix, mix, \amp, 1, \out, 0, \dur, total_dur+reverbtime, \gate, 1, \time_interval, time_interval, \start_point, start_point, \target, target, \doneAction, 14], group);

	delay = Synth(\delay, [\in, dbus, \out, rbus, \time_interval, 0.2, \delaytime, dt, \decaytime, dd, \amp, 1, \dur, 10, \gate, 1], group);
	instruments.do({
		arg item, i;
		var p;
		if(item == 'wavetable', {
			p = ~build_wavetable_pattern.value(vals, group, dbus);
			~build_wave_table_fork.value(total_dur, reverbtime, p);
		}, {
			p = ~gm.at(item).value(vals, group, dbus);
			~build_inst_fork.value(p);
		});

		// Free buses after a time.
	});
	{
		(reverbtime+total_dur+0.1).wait;
		rbus.free;
		dbus.free;
	}.fork;
};

~get_delay_values = {
	arg array;
	array[1..2];
};

~get_reverb_values = {
	arg array;
	array[3..6]
};

~get_spat_values = {
	arg array;
	array[7..9];
};

~get_mod_values = {
	arg array;
	array[10..11];
};

~get_octave_value = {
	arg array;
	array[12];
};

~get_total_dur_value = {
	// old name is time interval
	arg array;
	array[13];
};

~get_instrument_names = {
	arg array;
	var names_len = array[14];
	array[15..(15+names_len-1)];
};

~get_chords_data = {
	arg array;
	var names_len, c1_len, c2_len, c3_len, c1, c2, c3, cw1, cw2, cw3;
	names_len = array[14];
	cw1 = array[names_len+15];
	c1_len = array[names_len+16].asInteger;
	c1 = array[(17 + names_len)..(16 + names_len + c1_len)];
	cw2 = array[17 + names_len + c1_len];
	c2_len = array[18 + names_len + c1_len].asInteger;
	c2 = array[(19 + names_len + c1_len)..(18 + names_len + c1_len + c2_len)];
	cw3 = array[(19 + names_len + c1_len + c2_len)];
	c3_len = array[(20 + names_len + c1_len + c2_len)].asInteger;
	c3 = array[((21 + names_len + c1_len + c2_len))..((20 + names_len + c1_len + c2_len + c3_len))];
	[[c1, c2, c3], [cw1, cw2, cw3]];
};

~get_rhythm_data = {
	arg array;
	var names_len, c1_len, c2_len, c3_len, rdata;
	names_len = array[14];
	c1_len = array[names_len+16].asInteger;
	c2_len = array[18 + names_len + c1_len].asInteger;
	c3_len = array[(20 + names_len + c1_len + c2_len)].asInteger;
	rdata = array[(21 + names_len + c1_len + c2_len + c3_len)..]
};

~build_dur_Pseq = {
	arg array, total_dur;
	var pseq;
	pseq = Pseq(
		array.collect({
			arg item, i;
			if(item < 0, {
				Rest((total_dur / array.size) / 2);
			}, {
				(total_dur / array.size) / 2;
			})
		}), 1);
	pseq;
};

~build_notes_Pwrand = {
	arg chords_data;
	var pwrand;
	pwrand = Pwrand(
		chords_data[0].collect({ arg item, i; Prand(item, inf)}),
		chords_data[1],
		inf
	);
};

~build_wave_table_fork = {
	arg dbus, rbus, total_dur, reverbtime, wavetable_buf_pattern;
	{
		(reverbtime+total_dur+0.1).wait;
		// free wave table buffers
		wavetable_buf_pattern[1].free;
	}.fork;

	// play wave table patterns
	wavetable_buf_pattern[0].play;
};

~build_inst_fork = {
	arg inst_pattern;
	inst_pattern.play;
};



)
