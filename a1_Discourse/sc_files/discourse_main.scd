(
var path;
path = thisProcess.nowExecutingPath.dirname;

o = Server.default.options;
o.memSize = 16384;
o.maxNodes = 4096;
s = Server.default;


s.waitForBoot(
	{
		~gm = Dictionary.new();
		~netaddress = NetAddr.new("127.0.0.1", 57120);
		thisProcess.interpreter.executeFile(path +/+ "/discourse_synthdefs.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_pattern_builders.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_helper_functions.scd");
		thisProcess.interpreter.executeFile(path +/+ "/discourse_init.scd");
		~discourse_init.value(~gm, s, 10);
		thisProcess.interpreter.executeFile(path +/+ "/discourse_oscfuncs.scd");
	}
);
)

~buildSignalPath.value([ 'sound_triggers', 15, 8, 0.0, 0.9383333325386, 0.061666667461395, 0.1203999966383, 6.5357141494751, 0.1203999966383, 0.0, 0.0, 0.0, 4, 10, 4, 'wavetable1', 'sin', 'saw', 'saw', 0.6691871881485, 3.0, 0.0, 3.0, 7.0, 0.49402922391891, 3.0, 0.0, 4.0, 9.0, 0.83678364753723, 3.0, 0.0, 5.0, 8.0, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5 ]);

