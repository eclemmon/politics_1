(
var path;
path = thisProcess.nowExecutingPath.dirname;
~server = Server.default;

~server.waitForBoot(
	{
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_synthdefs.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_functions.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_oscfuncs.scd");
		~server.sync;
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_init.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_routine.scd");
	};

);
~main.value();
)



~attack.value(~gm, -1.233);