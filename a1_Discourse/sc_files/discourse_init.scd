(

~discourse_init = {
	arg memory, server, granBufLength;
	var buffer, soundInRouter, pointer, recBuf;
	buffer = ~buildGranulatorBuffer.value(~server, granBufLength);
	memory.put(\granBuffer, buffer);
	memory.put(\inputBus, Bus.audio(~server, 1));
	memory.put(\ptrBus, Bus.audio(~server, 1));
	memory.put(\inputGroup, Group.new);
	memory.put(\ptrGroup, Group.after(memory.at(\granulator_mem).at(\inputGroup)));
	memory.put(\recGroup, Group.after(memory.at(\granulator_mem).at(\ptrGroup)));
	memory.put(\granGroup, Group.after(memory.at(\granulator_mem).at(\recGroup)));
	soundInRouter = Synth(\soundInRouter, [\in, 0, \out, memory.at(\inputBus)], memory.at(\inputGroup));
	memory.put(\soundInRouter, soundInRouter);
	pointer = Synth(\pointer, [\buf, memory.at(\granBuffer), \out, memory.at(\ptrBus)], memory.at(\ptrGroup));
	memory.put(\pointer, pointer);
	recBuf = Synth(\recordBuffer, [\ptrIn, memory.at(\ptrBus), \recIn, memory.at(\inputBus), \buf, memory.at(\granBuffer)], memory.at(\recGroup));
	memory.put(\recBuf, recBuf);
	memory.put(\wtBuffers, ~makeWtBuffers.value());
	true;
};

)