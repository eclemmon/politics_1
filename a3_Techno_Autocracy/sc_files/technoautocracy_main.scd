(
// #####################################################################################################################
// technoautocracy_init.scd
// ---------------------------------------------------------------------------------------------------------------------
// This file initializes all the program files for the technoautocracy movement.
// ---------------------------------------------------------------------------------------------------------------------
// The logic of the work works as follows:
// There are two health reservoirs for the technoautocarcy: one for sin waves (autocratic utopia) and another
// anti-Human instruments.
// The piece begins with noisy, quick switches, and then settles into randomly selecting between anti-human elements
// during the main routine. The sin waves start as off. When the anti-human instrument's amplitude reaches their
// maximum 'health', the machine begins a second phase, where the sin waves gradually creep in. When the sin waves'
// 'health' is full the anti-human instruments fall off. When the anti-human instruments are silent at this point,
// the LFOs on the sin wave's phase converge. When all the phases of the LFOs line up, all the different pitches
// glissando over 5 minutes to a single pitch.
// ---------------------------------------------------------------------------------------------------------------------
// When the machine is attacked, depending on the current phase of the movement the reactive program is in, either
// sin waves go down or anti-human instruments lose health. The machine then responds with an aggressive sound and
// pauses healing. The attack sound is piano with delay and harmonic content from No Future Without Forgiveness
// (https://www.youtube.com/watch?v=JUDL-mVfRKE). The attacks add an 'attack' token to a queue, which pauses the
// machine's healing until the queue is empty. If a user supports the machine, it adds to the health of the machine and
// pops an attack token off the queue.
// #####################################################################################################################

var path;
path = thisProcess.nowExecutingPath.dirname;
~server = Server.default;

// Boot the server and execute all program files.
~server.waitForBoot(
	{
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_synthdefs.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_functions.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_oscfuncs.scd");
		~server.sync;
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_init.scd");
		thisProcess.interpreter.executeFile(path +/+ "/technoautocracy_routine.scd");
		~server.sync;

	};

);

)

(
// #####################################################################################################################
// Start the piece here when ready.
// #####################################################################################################################

~main.value();
)

(
// #####################################################################################################################
// Sometimes you just really need to rage against the machine, but not via text or tweet.
// #####################################################################################################################

~attack.value(~gm, -1.233);
~support.value(~gm, 1.233);
)