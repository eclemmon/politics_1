(
// #####################################################################################################################
// discourse_helper_functions.scd
// ---------------------------------------------------------------------------------------------------------------------
// A set of helper functions for parsing and building variables for the big function in discourse_build_sig_path.scd
// #####################################################################################################################

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
	arg array;
	array[13];
};

~get_instrument_names = {
	arg array;
	var names_len = array[14];
	array[15..(15+names_len-1)];
};

~get_chords_data = {
    // A little bit trickier converting incoming OSC data into usable arrays.
    // For future — learn how to build this data in Int8Arrays, as SC can accept them. Current implementation
    // of OSCFunc in SuperCollider doesn't like arrays from python-osc very much.
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
    // A little bit trickier converting incoming OSC data into usable arrays.
    // For future — learn how to build this data in Int8Arrays, as SC can accept them. Current implementation
    // of OSCFunc in SuperCollider doesn't like arrays from python-osc very much.
	arg array;
	var names_len, c1_len, c2_len, c3_len, rdata;
	names_len = array[14];
	c1_len = array[names_len+16].asInteger;
	c2_len = array[18 + names_len + c1_len].asInteger;
	c3_len = array[(20 + names_len + c1_len + c2_len)].asInteger;
	rdata = array[(21 + names_len + c1_len + c2_len + c3_len)..]
};

~build_dur_Pseq = {
    // Builds a Pseq of durations. Parses durations for '/r' key to identify rests.
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
    // Uses weighted chord data to randomly select next notes.
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
    // Builds an array of values that indicates the length that each note sustains after attacks.
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
    // Builds a string, helpful for debugging and checking on sound synthesis data.
	arg vals;
	var string;
	string = "
#########################################
Total Duration: %
Delay Values: %
Reverb Values: %
Spatialization Values: %
Instruments: %
Time Interval of Events: %
Duration: %
Octave: %
Rhythm: %
Sustain Values: %
#########################################
".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9]);
	string;
};



)
