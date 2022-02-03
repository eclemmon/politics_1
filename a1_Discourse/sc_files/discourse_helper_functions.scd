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
	pwrand;
};

~build_sus_data = {
	arg array, total_dur;
	var pseq, sus_vals;
	sus_vals = array.separate({arg a, b; (a != b) && (b > 0)});
	sus_vals = sus_vals.collect({
		arg item, i;
		item.size
	});
	sus_vals;
};

~print_vals = {
	arg vals;
	var string;
	string = "
#################################
Total Duration: %
Delay Values: %
Reverb Values: %
Spatialization Values: %
Instruments: %
Time Interval of Events: %
Duration: %
Octave: %
#################################
".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7]);
	string;
};

)
