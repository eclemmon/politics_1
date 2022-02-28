(
~mainRoutine = Routine.new({
	var aHumMax;
	loop {
		var inst;
		inst = ~gm.at(\antiHumanInstrumentKeys).choose;

		if(~gm.at(\pureSins) != true, {
			// Change the instrument
			~changeAntiHumanInstrument.value(
				~gm,
				~gm.at(\currentAntiHumanInstrument),
				inst,
				~gm.at(\antiHumanAmpVal) / 2
			);

			// Update Visuals
			~sendChangeVisuals.value(~gm, ~gm.at(\antiHumanInstrumentKeys).indexOf(inst));
		}, {
			if (~gm.at(\finalSynthsFreed) != true, {
				~gm.at(\antiHumanInst).do({arg item, i; item.set(\gate, 0);});
				~gm.at(\antiHumanBaseNoise).do({arg item, i; item.set(\gate, 0);});
				~gm.put(\finalSynthsFreed, true)
			})
		};
		);

		// if attack queue is empty set \antiHumanHealing boolean to true
		~resumeHealing.value(~gm);

		// Heal antiHuman
		if(~gm.at(\antiHumanHealing), {
			// Heal the amplitude by 0.01
			~heal.value(~gm);
		});

		// Print for testing
		~gm.at(\antiHumanAmpVal).postln;
		~gm.at(\sinAmpVal).postln;
		// Wait between 1 and 3 seconds
		rrand(1, 3).wait;

	}.fork;

});

~introduction = Routine.new({
	var inst, resist, resistTime, stop, stopTime;

	// Play the antiHuman instruments
	5.do({
		inst = ~gm.at(\antiHumanInstrumentKeys).choose;
		// Change the instrument
		~changeAntiHumanInstrument.value(
			~gm,
			~gm.at(\currentAntiHumanInstrument),
			inst,
			~gm.at(\antiHumanAmpVal) / 2
		);

		// Update Visuals
		~sendChangeVisuals.value(~gm, ~gm.at(\antiHumanInstrumentKeys).indexOf(inst));
		rrand(3, 5).wait;
	});

	// Free Anti Human inst
	~gm.at(\antiHumanInst).do({arg item, i; item.set(\gate, 0); });
	~gm.at(\antiHumanBaseNoise).do({arg item, i; item.set(\gate, 0) });

	// Set visuals to black
	~sendVisualsIntroWhite.value(~gm, true);

	// Play You can resist
	resist = ~gm.at(\introBuffers).at(0);
	resistTime = resist.numFrames / ~server.sampleRate;
	Synth(\playback, [\pos, 0, \buf, resist, \amp, 4]);

	resistTime.wait;

	// Set visuals to normal routine
	~sendVisualsIntroWhite.value(~gm, false);

	// Resume Base Noise
	~gm.put(\antiHumanBaseNoise, Array.fill(8, {arg i; Synth(\lowClip,
				[\out, 0, \amp, 1, \filter_freq, i*10+40, \pos, 1.0.rand2]
	)}));

	// Play AntiHuman instruments
	~gm.put(\antiHumanInst, ~buildAntiHumanInstrumentArray.value(\gendy, 0.5));
	~gm.put(\currentAntiHumanInstrument, \gendy);
	rrand(1,3).wait;

	// Play Anti Human instruments
	9.do({
		inst = ~gm.at(\antiHumanInstrumentKeys).choose;
		// Change the instrument
		~changeAntiHumanInstrument.value(
			~gm,
			~gm.at(\currentAntiHumanInstrument),
			inst,
			~gm.at(\antiHumanAmpVal) / 2
		);

		// Update Visuals
		~sendChangeVisuals.value(~gm, ~gm.at(\antiHumanInstrumentKeys).indexOf(inst));
		rrand(1, 3).wait;
	});

	// Free Anti Human inst
	~gm.at(\antiHumanInst).do({arg item, i; item.set(\gate, 0); });
	~gm.at(\antiHumanBaseNoise).do({arg item, i; item.set(\gate, 0); });

	// Set visuals to black
	~sendVisualsIntroWhite.value(~gm, 1);

	// Play Tell it to stop
	stop = ~gm.at(\introBuffers).at(1);
	stopTime = stop.numFrames / ~server.sampleRate;
	Synth(\playback, [\pos, 0, \buf, stop, \amp, 4]);
	stopTime.wait;

	// Set visuals to normal routine
	~sendVisualsIntroWhite.value(~gm, 0);

	// Resume Base Noise
	~gm.put(\antiHumanBaseNoise, Array.fill(8, {arg i; Synth(\lowClip,
				[\out, 0, \amp, 1, \filter_freq, i*10+40, \pos, 1.0.rand2]
	)}));

	// Play AntiHuman instruments
	~gm.put(\antiHumanInst, ~buildAntiHumanInstrumentArray.value(\gendy, 0.5));
	~gm.put(\currentAntiHumanInstrument, \gendy);
	rrand(3, 5).wait;

	4.do({
		// select the instrument
		inst = ~gm.at(\antiHumanInstrumentKeys).choose;
		// Change the instrument
		~changeAntiHumanInstrument.value(
			~gm,
			~gm.at(\currentAntiHumanInstrument),
			inst,
			~gm.at(\antiHumanAmpVal) / 2
		);

		// Update Visuals
		~sendChangeVisuals.value(~gm, ~gm.at(\antiHumanInstrumentKeys).indexOf(inst));
		rrand(3, 5).wait;
	});

	// Change introduction boolean
	~gm.put(\introduction, false);

	// Call main logic function
	~main.value();
});

)







// 2 Resevoirs, Sin Waves and Anti-Human elements
// When attacked, sin waves go down, anti-human elements Go down, and then respond more aggressively, then return to a lower state, then start healing. Attack sound is piano w/ delay + chords from No Future.

// Randomly choose between different synths and switch between.
/*
Piece begins with noisy, quick switches, then settles into random selecting between anti-human elements routine.
Anti-Human

Sin Waves (peel off from all elements).
~the sin waves start as off.
~They gradually creep in whenever the Anti-human elements reach their peak
~When reach peak, aHum falls off
~when aHum is out entirely, Sin LFOs narrow down to pure sin wave
~when only pure sin waves, 5 minute gliss to single pitch.

Anti-Human elements
~bitCrush
~StandardN Noise
~LowClip


*/
