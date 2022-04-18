(
// #####################################################################################################################
// discourse_main.scd
// ---------------------------------------------------------------------------------------------------------------------
// Boots the scsynth server and executes all project files.
// #####################################################################################################################
var path;

// Path to discourse_main.scd
path = thisProcess.nowExecutingPath.dirname;

// Set server options
o = Server.default.options;
o.memSize = 16384;
o.maxNodes = 4096;
o.maxSynthDefs = 4096;
s = Server.default;

s.waitForBoot(
	{
	    // Init Global memory
		~gm = Dictionary.new();

		// Init local net address for incoming OSC data
		~netaddress = NetAddr.new("127.0.0.1", 57120);

		// Init project files
		thisProcess.interpreter.executeFile(path +/+ "/discourse_synthdefs.scd");
		s.sync;
		thisProcess.interpreter.executeFile(path +/+ "/discourse_pattern_builders.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_helper_functions.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_build_sig_path.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_init.scd");
		~discourse_init.value(~gm, s, 10);
		thisProcess.interpreter.executeFile(path +/+ "/discourse_oscfuncs.scd");
	}
);
)