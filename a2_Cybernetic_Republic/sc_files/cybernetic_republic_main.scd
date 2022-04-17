(
// Set path directory.
var path;
path = thisProcess.nowExecutingPath.dirname;
// Boot sc program files.
thisProcess.interpreter.executeFile(path +/+ "/cybernetic_republic_init.scd");
thisProcess.interpreter.executeFile(path +/+ "/cybernetic_republic_helper_functions.scd");
thisProcess.interpreter.executeFile(path +/+ "/cybernetic_republic_osc_funcs.scd");
)