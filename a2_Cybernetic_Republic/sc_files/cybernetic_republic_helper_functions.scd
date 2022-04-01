(

~add_midinotes_durations_to_dict = {
	arg mem, key, midinotes, durations;
	// mem.at(key) should be of List class
	// Adds an incoming array to the end of the list.
	mem.at(key).add(Dictionary[\midinotes -> midinotes, \durations-> durations]);
};


~clear_midinotes_durations_at_key = {
	arg mem, key;
	mem.put(key, List.new());
};

~build_ppar = {
	arg mem, key, mOutAddress;
	var ppar_array, ppar;
	ppar_array = List.new();
	mem.at(key).do({
		arg item, i;
		ppar_array.add(
			Pbind(
				\type, \midi,
				\midiout, mem.at(\mOuts).at(mOutAddress),
				\midinote, Pseq(item.at(\midinotes), inf),
				\dur, Pseq(item.at(\durations), inf),
				\amp, 1
			);
		);
	});
	ppar = Pdef(key, Ppar(ppar_array, inf));
	ppar;
};

)