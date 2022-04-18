(
// #####################################################################################################################
// discourse_init.scd
// ---------------------------------------------------------------------------------------------------------------------
// Takes in global memory object and adds midi information to it.
// #####################################################################################################################

~discourse_init = {
	arg memory;
	// Store instrument midi channels
	memory.put(\channels, Array.fill(16, {arg i; i }));
	memory.put(\mOutIndex, 0);
	memory.put(\mOut, Array.fill(8, {arg i; MIDIOut.new(i)}));
	memory.put(\panRoutines, Array.fill(8, {arg i; Routine({})}));
	memory.put(\panChannels, Array.with(20, 21, 22, 23, 24, 25, 26, 27));
	true;
};

~discourse_init.value(~gm);
)
