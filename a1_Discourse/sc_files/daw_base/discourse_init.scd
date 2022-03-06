(


~discourse_init = {
	arg memory;
	// Store instrument midi channels
	memory.put(\channels, Array.fill(16, {arg i; i }));
	memory.put(\mOutIndex, 0);
	memory.put(\mOut, Array.fill(8, {arg i; MIDIOut.new(i)}));
	true;
};

~discourse_init.value(~gm);
)
