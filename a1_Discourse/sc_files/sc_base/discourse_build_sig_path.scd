(
~buildSignalPath = {
	arg vals, memory;
	var reverb, spat, delay, synths, group, pattern, total_dur, dvals, rvals, spatvals, dt, dd, predelay, reverbtime, lpf, mix, start_point, target, time_interval, instruments, patterns, splitter, sbus, rbus, dbus, fbus, spatbus, octave, filter, rhythm, sus_vals;
	total_dur = ~get_total_dur_value.value(vals);
	dvals = ~get_delay_values.value(vals);
	rvals = ~get_reverb_values.value(vals);
	spatvals = ~get_spat_values.value(vals);
	instruments = ~get_instrument_names.value(vals);
	octave = ~get_octave_value.value(vals);
	rhythm = ~get_rhythm_data.value(vals);
	sus_vals = ~build_sus_data.value(rhythm, total_dur);

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

	~print_vals.value([total_dur, dvals, rvals, spatvals, instruments, time_interval, total_dur, octave, rhythm, sus_vals]).postln;

	// Automatically allocate buses
	rbus = memory.at('rbus');
	dbus = memory.at('dbus');
	fbus = Bus.audio(s, numChannels: 1);
	spatbus = Bus.audio(s, numChannels: 1);
	sbus = Bus.audio(s, numChannels: 2);

	// Synths
	group = memory.at('synthgroup');
	splitter = Synth(\splitter, [\in, sbus, \out1, rbus, \out2, dbus, \dur, total_dur, \gate, 1], memory.at(\splittergroup));
	spat = Synth(\linear_spat_motion, [\in, spatbus, \out, sbus, \time_interval, time_interval, \start_point, start_point, \target, target, \dur, total_dur, \gate, 1], memory.at(\spatgroup));
	filter = Synth(\notch_filters, [\in, fbus, \out, spatbus, \dur, total_dur, \amp, 1, \rq, 0.3], memory.at(\spatgroup));

	patterns = instruments.collect({
		arg item, i;
		var p, bufs;
		if(item.asString.contains("wavetable"), {
			bufs = ~gm.at(item).value(item);
			p = ~build_wavetable_pattern.value(vals, group, fbus, bufs);
		}, {
			if(item.asString.contains("grain"), {
				p = ~build_grain_pattern.value(vals, group, fbus, memory);
			}, {
				if((item.asString.contains("sin") || item.asString.contains("peep") || item.asString.contains("subtract")), {
					p = ~gm.at(item).value(vals, group, spatbus);
				}, {
					p = ~gm.at(item).value(vals, group, fbus);
				});

			});
		});
	});

	// Parallel play patterns
	Ppar(patterns).play;

	// Free buses after a time.
	{
		(total_dur+0.5).wait;
		sbus.free;
		spatbus.free;
		fbus.free;
		splitter.free;
		// spat.free;
		// group.free;
	}.fork;
};
)