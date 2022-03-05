(

~discourse_init = {
	arg memory, server, granBufLength;
	var buffer, soundInRouter, pointer, recBuf;

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
	memory.put(\mOuts, Array.fill(MIDIClient.destinations.size, {arg i; MIDIOut.new(i) }));
	true;
};

)

