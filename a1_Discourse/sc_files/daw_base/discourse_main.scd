(
// #####################################################################################################################
// discourse_main.scd
// ---------------------------------------------------------------------------------------------------------------------
// Boots MIDIClient, and all files in daw_base by path.
// #####################################################################################################################

var path;

// Path to discourse_main.scd
path = thisProcess.nowExecutingPath.dirname;

// Init MIDIClient
MIDIClient.init;

// Init Global memory
~gm = Dictionary.new();

// Init local net address for incoming OSC data
~netaddress = NetAddr.new("127.0.0.1", 57120);
~osc_boot_address = NetAddr.new("127.0.0.1", 12645);

// Init project files
thisProcess.interpreter.executeFile(path +/+ "/discourse_midi_cc_functions.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_helper_functions.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_build_sig_path.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_init.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_oscfuncs.scd");
~osc_boot_address.sendMsg("/supercollider_ready", true);
)
