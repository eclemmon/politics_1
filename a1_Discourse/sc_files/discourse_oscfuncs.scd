(
OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	~buildSignalPath.value(args, ~gm);
	"######################################".postln;
}, '/sound_triggers');
)

/*
[
OSC NAME
'/sound_triggers',

DELAY Feedback Delay Time, Delay Decay — 2 VALUES
15, 8,

REVERB predelay, reverbtime, lpf, mix — 4 VALUES
0.0, 0.9383333325386, 0.061666667461395, 0.1203999966383,

SPATIALIZATION Time Interval, Start Point, Target — 3 VALUES
6.5357141494751, 0.1203999966383, 0.0,

MODULATION Freq, Amp — 2 VALUES
0.0, 0.0,

OCTAVE — 1 VALUE
1,

TIME INTERVAL DATA
6.5357141494751,

INSTRUMENT NAMES — VAR VALUES
4, 'square', 'sin', 'impulse', 'sin',

WEIGHT OF CHORDS, SIZE OF CHORDS AND NOTES — VAR VALUES
0.6691871881485, 3.0, 4.0, 7.0, 11.0, 0.49402922391891, 3.0, 1.0, 5.0, 10.0, 0.83678364753723, 3.0, 1.0, 6.0, 9.0,

RHYTHM
1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5, 1.0, -1.5, -1.5, -1.5, 1.0, -1.5, -1.5 ]
*/

