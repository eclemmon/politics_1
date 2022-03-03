
(
~server.waitForBoot({
	~gm = Dictionary.newFrom(
		[
			\recv_netaddress, NetAddr.new("127.0.0.1", 57120),
			\visuals_netaddress, NetAddr.new("127.0.0.1", 12000),
			\visual_selection, 0,

			// Maximum amplitude values
			\antiHumanMax, 1,
			\sinMax, 0.4,

			// Anti human instruments
			\antiHumanInst, ~buildAntiHumanInstrumentArray.value(\bitCrush, 0), // HERE GOES THE ANTI HUMAN inst
			\antiHumanBaseNoise, Array.fill(8, {arg i; Synth(\lowClip,
				[\out, 0, \amp, 0, \filter_freq, i*10+40, \pos, 1.0.rand2]
			)}),

			// Sin tones
			\sin, Array.fill(8, {arg i;
				Synth(\sin, [\out, 0, \amp, 0, \freq, (36 + (i*4) + i).midicps, \pos, 1.0.rand2, \lfoPhase, (i * 0.123), \gate, 1, \sinLFOFreq, (0.1 * i)]);
			}),

			\currentAntiHumanInstrument, \bitCrush,
			\antiHumanAmpVal, 0.5, //init current val
			\sinAmpVal, 0, // init Sin val
			\sinLFOPhase,  0.123,
			\sinLFOFreq, 0.1,

			// Multipliers for attacks and supports (should be set initially by number of audience members?)
			\baseAtkMul, 0.05,
			\baseSuptMul, 0.01,

			// Sectional
			\antiHumanHealing, true,
			\antiHumanResponding, false,
			\introduction, true,
			\audienceDefeated, false,
			\sinHealing, false,
			\audienceWon, false,
			\sinMaxed, false,
			\pureSins, false,
			\finalSynthsFreed, false,
			\glissActivated, false,

			// Data control
			\attackQueue, PriorityQueue.new,
			\antiHumanInstrumentKeys, [\bitCrush, \standardNNoise, \gendy, \sin],
			\responseBuffers, ~buildResponseBuffers.value("/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Resources/soundfiles/responses"),
			\attackBuffers, ~buildResponseBuffers.value("/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Resources/soundfiles/attacks"),
			\introBuffers, ~buildResponseBuffers.value("/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Resources/soundfiles/introduction"),
			\audienceWonBuffer, Buffer.readChannel(~server, "/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Misc/audience_won/SC_220227_224251.aiff", channels: [0,1])
		]
	);

});
)
