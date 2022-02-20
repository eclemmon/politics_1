
(
~server = Server.default;
~server.waitForBoot({
	~gm = Dictionary.newFrom(
		[
			\antiHumanMax, 1,
			\antiHumanInst, ~buildAntiHumanInstrumentArray.value(\bitCrush, 0.5), // HERE GOES THE ANTI HUMAN inst
			\antiHumanBaseNoise, Array.fill(8, {arg i; Synth(\lowClip,
				[\out, 0, \amp, 0.5, \filter_freq, i*10+40, \pos, 1.0.rand2]
			)}),
			\sin, Array.fill(8, {arg i;
				Synth(\sin, [\out, 0, \amp, 0, \freq, (36 + (i*4) + i).midicps, \pos, 1.0.rand2, \lfoPhase, (i * 0.123), \gate, 1, \sinLFOFreq, (0.1 * i)]);
			}), // Here goes the sin tones
			\currentAntiHumanInstrument, \bitCrush,
			\antiHumanAmpVal, 0.5, //init current val
			\sinAmpVal, 0, // init Sin val
			\sinLFOPhase,  0.123,
			\sinLFOFreq, 0.1,
			\unhookStandardN, [0, 1, 2],

			\baseAtkMul, 0.05,
			\baseSuptMul, 0.01,

			\antiHumanHealing, true,
			\antiHumanResponding, false,
			\antiHumanMaxed, false,
			\antiHumanOut, false,
			\audienceDefeated, false,
			\sinOff, true,
			\sinMaxed, false,
			\pureSins, false,
			\finalSynthsFreed, false,
			\glissActivated, false,

			\attackQueue, PriorityQueue.new,
			\antiHumanInstrumentKeys, [\bitCrush, \standardNNoise, \gendy, \sin],
		]
	);

});
)
