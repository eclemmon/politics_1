(

~add_midinotes_durations_to_dict = {
	arg mem, key, midinotes, durations;
	// mem.at(key) should be of List class
	// Adds an incoming array to the end of the list.
	mem.at(key).add(\midinotes, midinotes);
	mem.at(key).add(\durations, durations);
};

~add_midinotes_to_dict = {
	arg mem, key, midinotes;
	mem.at(key).put(\midinotes, midinotes);
};

~add_durations_to_dict = {
	arg mem, key, durations;
	mem.at(key).put(\durations, durations);
};

~parse_rests_and_notes = {
	arg array;
	var notes_and_rests;
	notes_and_rests = Array.fill(array.size, {
		arg i;
		if((array[i].asString.beginsWith("/r")), {
			if(array[i] == '/r', {
				Rest(0.25);
			}, {
				Rest(array[i].asString[2..].asFloat);
			});
		}, {
			array[i];
		});
	});
};

~clear_voice = {
	arg mem, key;
	mem.put(key, Dictionary.newFrom([\durations, List.new(), \midinotes, List.new()]));
};

~clear_midinotes_durations_at_key = {
	arg mem, key;
	mem.put(key, List.new());
};

~build_ppar = {
	arg mem, key, mOutAddress, chan=0;
	var ppar_array, ppar;
	ppar_array = List.new();
	// mem.at(key).at(\midinotes).postcs;
	mem.at(key).at(\midinotes).do({
		arg item, i;
		ppar_array.add(
			Pbind(
				\type, \midi,
				\midiout, mem.at(\mOuts).at(mOutAddress),
				\midinote, Pseq(mem.at(key).at(\midinotes).at(i), inf),
				\dur, Pseq(mem.at(key).at(\durations).at(i), inf),
				\amp, 1,
				\chan, chan,
				\visualcontrol, Pfunc({~send_osc_message.value(mem, key, 0)})
			);
		);
	});
	ppar = Pdef(key, Ppar(ppar_array, inf));
	ppar;
};


~build_pattern = {
	arg mem, key, mOutAddress, chan=0;
	var pattern;
	pattern = Pbind(
		\type, \midi,
		\midiout, mem.at(\mOuts).at(mOutAddress),
		\midinote, Pseq(mem.at(key).at(\midinotes), inf),
		\dur, Pseq(mem.at(key).at(\durations), inf),
		\amp, 1,
		\chan, chan,
		\visualcontrol, Pfunc({~send_osc_message.value(mem, key, 0)})
	);
	pattern = Pdef(key, pattern);
	pattern;
};

~send_osc_message = {
	arg mem, address, msg;
	mem.at(\visuals_netaddress).sendMsg(address, msg);
};
)