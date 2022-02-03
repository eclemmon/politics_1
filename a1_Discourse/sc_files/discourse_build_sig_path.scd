(
~buildSignalPath = {
	arg vals, memory;
	var reverb, spat, delay, synths, group, pattern, total_dur, dvals, rvals, spatvals, dt, dd, predelay, reverbtime, lpf, mix, start_point, target, time_interval, instruments, patterns, splitter, sbus, rbus, dbus, octave;
	total_dur = ~get_total_dur_value.value(vals);
	dvals = ~get_delay_values.value(vals);
	rvals = ~get_reverb_values.value(vals);
	spatvals = ~get_spat_values.value(vals);
	instruments = ~get_instrument_names.value(vals);
	octave = ~get_octave_value.value(vals);

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

	~print_vals.value([total_dur, dvals, rvals, spatvals, instruments, time_interval, total_dur, octave]).postln;

	// Automatically allocate buses

	rbus = memory.at('rbus');
	dbus = memory.at('dbus');
	sbus = Bus.audio(s, numChannels: 2);

	// Synths
	group = Group.new;
	splitter = Synth(\splitter, [\in, sbus, \out1, rbus, \out2, dbus, \dur, total_dur, \gate, 1], group);

	patterns = instruments.collect({
		arg item, i;
		var p, bufs;
		if(item.asString.contains("wavetable"), {
			item.postln;
			bufs = ~gm.at(item).value(item);
			p = ~build_wavetable_pattern.value(vals, group, sbus, bufs);
		}, {
			p = ~gm.at(item).value(vals, group, sbus);
		});
	});

	// Parallel play patterns
	Ppar(patterns).play;

	// Free buses after a time.
	{
		(total_dur+0.1).wait;
		sbus.free;
		group.free;
	}.fork;
};
)