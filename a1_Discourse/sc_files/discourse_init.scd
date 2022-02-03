(

~discourse_init = {
	arg memory, server, granBufLength;
	var buffer, soundInRouter, pointer, recBuf;
	buffer = ~buildGranulatorBuffer.value(server, granBufLength);
	memory.put(\granBuffer, buffer);
	memory.put(\inputBus, Bus.audio(server, 1));
	memory.put(\ptrBus, Bus.audio(server, 1));
	memory.put(\inputGroup, Group.new);
	memory.put(\ptrGroup, Group.after(memory.at(\inputGroup)));
	memory.put(\recGroup, Group.after(memory.at(\ptrGroup)));
	memory.put(\granGroup, Group.after(memory.at(\recGroup)));
	soundInRouter = Synth(\soundInRouter, [\in, 0, \out, memory.at(\inputBus)], memory.at(\inputGroup));
	memory.put(\soundInRouter, soundInRouter);
	pointer = Synth(\pointer, [\buf, memory.at(\granBuffer), \out, memory.at(\ptrBus)], memory.at(\ptrGroup));
	memory.put(\pointer, pointer);
	recBuf = Synth(\recordBuffer, [\ptrIn, memory.at(\ptrBus), \recIn, memory.at(\inputBus), \buf, memory.at(\granBuffer)], memory.at(\recGroup));
	memory.put(\recBuf, recBuf);
	memory.put(\wtBuffers, ~makeWtBuffers.value());
	memory.put('square', ~build_square_pattern);
	memory.put('sin', ~build_sin_pattern);
	memory.put('impulse', ~build_impulse_pattern);
	memory.put('saw', ~build_saw_pattern);
	memory.put('noise', ~build_noise_pattern);
	memory.put('wavetable1', ~makeWtBuffers.value());
	memory.put('wavetable2', ~makeWtBuffers.value());
	memory.put('wavetable3', ~makeWtBuffers.value());
	true;
};

)
// ~gm.at(\inputGroup);