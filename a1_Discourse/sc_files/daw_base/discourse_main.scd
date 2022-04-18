(
var path;
path = thisProcess.nowExecutingPath.dirname;

MIDIClient.init;
~gm = Dictionary.new();
~netaddress = NetAddr.new("127.0.0.1", 57120);
thisProcess.interpreter.executeFile(path +/+ "/discourse_midi_cc_functions.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_helper_functions.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_build_sig_path.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_init.scd");
thisProcess.interpreter.executeFile(path +/+ "/discourse_oscfuncs.scd");

)