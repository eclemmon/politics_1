(
~routine = Routine.new({
	var aHumMax;
	loop {
		var inst;
		inst = ~gm.at(\antiHumanInstrumentKeys).choose;

		if(~gm.at(\pureSins) != true, {
			~changeAntiHumanInstrument.value(
				~gm,
				~gm.at(\currentAntiHumanInstrument),
				inst,
				~gm.at(\antiHumanAmpVal)
			);
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
		// Wait between 0.1 and 2 seconds
		rrand(1, 3).wait;
	}.fork;

});

~routine.play();
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
