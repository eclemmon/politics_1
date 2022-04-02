(
OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	// args.postcs;
	~add_durations_to_dict.value(~gm, args[1], Array.fill(args[2..].size, {
		arg i;
		if((args[i+2] == '/r'), {
			Rest(0.25);
		}, {
			args[i+2];
		});
	})
	);

	"######################################".postln;
}, '/message');

OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	// Stop previous pattern
	~gm.at(args[2].asSymbol).stop;
	// Run the pattern
	~gm.put(args[2].asSymbol, ~build_ppar.value(~gm, args[1].asSymbol, args[2].asSymbol));
	~gm.at(args[2].asSymbol).play;
	// Empty the pattern list
	~clear_midinotes_durations_at_key.value(~gm, args[1].asSymbol);
	"######################################".postln;
}, '/init');


OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	// args.postcs;
	~add_midinotes_durations_to_dict.value(~gm, \break_beat_1, Array.fill(args[2..].size, {arg i; args[1]}), Array.fill(args[2..].size, {
		arg i;
		if((args[i+2].asString.beginsWith("/r")), {
			if(args[i+2] == '/r', {
				Rest(0.25);
				0.25.postln;
			}, {
				Rest(args[i+2].asString[2..].asFloat);
				args[i+2].asString[2..].asFloat.postln;
			});
		}, {
			args[i+2];
		});
	})
	);

	"######################################".postln;
}, '/break_beat_1');

)

~gm.at(\break_beat_1).postcs;

~gm.at('rhythm').stop;
