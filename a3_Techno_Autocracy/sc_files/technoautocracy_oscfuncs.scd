(
// #####################################################################################################################
// technoautocracy_oscfuncs.scd
// ---------------------------------------------------------------------------------------------------------------------
// This file contains the relevant OSCFuncs to receiving and parsing data from python.
// #####################################################################################################################

OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	~attack.value(~gm, args[1]);
	"######################################".postln;
}, '/attack');

OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	~support.value(~gm, args[1]);
	"######################################".postln;
}, '/support');
)
