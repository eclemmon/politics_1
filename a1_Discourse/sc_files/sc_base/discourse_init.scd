(

~discourse_init = {
	arg memory, server, granBufLength;
	var buffer, soundInRouter, pointer, recBuf;
	// Init buses
	memory.put('rbus', Bus.audio(s, numChannels: 2));
	memory.put('dbus', Bus.audio(s, numChannels: 2));
	memory.put('spatbus', Bus.audio(s, numChannels:2));
	// Init reverb and delay
	memory.put('rdgroup', Group.new);
	memory.put('reverb', Synth(\reverb, [\in, memory.at('rbus'), \predelay, 1, \revtime, 5, \lpf, 4500, \mix, 0.5, \amp, 0.1, \out, 0], memory.at('rdgroup')));
	memory.put('delay', Synth(\delay, [\in, memory.at('dbus'), \out, memory.at('rbus'), \max_delay, 2, \delaytime, 0.1, \decaytime, 1, \amp, 0.1], memory.at('rdgroup')));
	// Init granulator buffer and pointer
	buffer = ~buildGranulatorBuffer.value(server, granBufLength);
	memory.put(\granBuffer, buffer);
	memory.put(\inputBus, Bus.audio(server, 1));
	memory.put(\ptrBus, Bus.audio(server, 1));
	memory.put(\inputGroup, Group.new);
	memory.put(\ptrGroup, Group.after(memory.at(\inputGroup)));
	memory.put(\recGroup, Group.after(memory.at(\ptrGroup)));
	soundInRouter = Synth(\soundInRouter, [\in, 0, \out, memory.at(\inputBus)], memory.at(\inputGroup));
	memory.put(\soundInRouter, soundInRouter);
	pointer = Synth(\pointer, [\buf, memory.at(\granBuffer), \out, memory.at(\ptrBus)], memory.at(\ptrGroup));
	memory.put(\pointer, pointer);
	recBuf = Synth(\recordBuffer, [\ptrIn, memory.at(\ptrBus), \recIn, memory.at(\inputBus), \buf, memory.at(\granBuffer)], memory.at(\recGroup));
	memory.put(\recBuf, recBuf);
	// Store instrument pattern calls
	memory.put('square', ~build_square_pattern);
	memory.put('sin', ~build_sin_pattern);
	memory.put('impulse', ~build_impulse_pattern);
	memory.put('saw', ~build_saw_pattern);
	memory.put('noise', ~build_noise_pattern);
	memory.put('peep', ~build_peep_pattern);
	memory.put('subtract', ~build_subtract_pattern);
	memory.put('wavetable1', ~makeWtBuffers.value());
	memory.put('wavetable2', ~makeWtBuffers.value());
	memory.put('wavetable3', ~makeWtBuffers.value());
	// Splitter group
	memory.put('splittergroup', Group.new);
	// Spat group
	memory.put('spatgroup', Group.new);
	// Synthesizer Group
	memory.put('synthgroup', Group.new);
	true;
};

)
// ~gm.at(\inputGroup);