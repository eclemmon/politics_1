(
// #####################################################################################################################
// technoautocracy_function.scd
// ---------------------------------------------------------------------------------------------------------------------
// This file holds a series of function controlling both the sound synthesis portion of the work, as well as some of
// the logic for reaction to attacks and supports from the audience.
// #####################################################################################################################

~attack = {
    // Steps through a series of functions that are called when the machine is attacked by an audience member.
	arg mem, updateVal;
	var attack_sound, instrument, timeToFreeInst;

	if(((mem.at(\audienceDefeated) != true) || (mem.at(\audienceWon) != true)), {
		// Attack Sound
		attack_sound = mem.at(\attackBuffers).choose;
		Synth(\playback, [\pos, 1.rand2, \buf, attack_sound, \amp, 3]);

		// Pause healing for a duration.
		mem.put(\antiHumanHealing, false);
		~pauseHealing.value(mem, updateVal);

		// calculate time to free responding synth
		timeToFreeInst = ~calculateTimeToFreeInst.value(updateVal);

		// Select response instrument
		instrument = [\playback].choose;

		// Set antiHuman to Responding
		mem.put(\antiHumanResponding, true);
		SystemClock.sched(0.5, { ~respond.value(mem, instrument, mem.at(\responseBuffers).choose, timeToFreeInst + 0.5); });

		// Decrement antiHumanAmpVal by updateVal
		~updateAHumOrSin.value(mem, updateVal * mem.at(\baseAtkMul));
	});

    // Finally boolean test whether the audience has won after this attack.
	~testAudienceWon.value(mem);
};

~testAudienceWon = {
    // Boolean tests whether the audience has won. If won, executes the "positive" ending sequence.
	arg mem;
	if(mem.at(\antiHumanAmpVal) <= 0, {
		if(mem.at(\audienceWon) != true, {
			"audience won".postln;
			mem.put(\audienceWon, true);
			~mainRoutine.stop();
			// PLAY END SEQUENCE
			Synth(\playback_2ch, [\buf, mem.at(\audienceWonBuffer)]);
			~sendVisualsAudienceWon.value(mem);
		});
	});

};

~support = {
    // This function supports the machine by adding the input value to the 'health bar'.
	arg mem, updateVal;
	// pop an attack off the pause healing queue
	mem.at(\attackQueue).pop;
	// updateVal should be positive. Adds the value to the antiHumanInsts/sins
	~updateAHumOrSin.value(mem, updateVal * mem.at(\baseSuptMul));
};

~heal = {
    // Called regularly by the main technoautocracy routine. Heals the 'health bar' of the machine.
	arg mem;
	if(mem.at(\audienceWon) != true, {
		// Heal 0.01
		~updateAHumOrSin.value(mem, 0.01);
		// Update Visuals
		~sendHeal2Visuals.value(mem, 1.0);
	});
};

~pauseHealing = {
    // Pauses the healing of the main technoautocracy routine on attack by putting a 'pause' into the attack queue.
    // schedules the \attackQueue to pop an attack token off in the future.
	arg mem, updateVal;
	var pauseTime, sum;
	// map updateVal:
	pauseTime = updateVal.linlin(0.0, 1.0, 1, 3.0);
	// put pause into attack queue
	mem.at(\attackQueue).put(pauseTime, pauseTime);
	sum = 0.0;
	mem.at(\attackQueue).do({arg i; sum = sum + i;});
	// schedule pop from attack queue based on pauseTime
	SystemClock.sched(sum, { mem.at(\attackQueue).pop; });
};

~resumeHealing = {
    // Tests if the attackQueue is empty of attack tokens. If so, resumes healing during the main teechnoautocracy
    // routine.
	arg mem;
	// If attack queue is empty, set antiHumanHealing to true.
	if(mem.at(\attackQueue).isEmpty, {
		mem.put(\antiHumanHealing, true);
	});
};

~updateAHumOrSin = {
    // Function that tests whether the health bar for the AntiHumanInstrument is full before updating sin values.
	arg mem, updateVal;
	// If \antiHumanAmplitudeValue is less than the preset AntiHuman amp maximum:
	if ((mem.at(\antiHumanAmpVal) < mem.at(\antiHumanMax)) && (mem.at(\sinMaxed) != true), {
		~updateAntiHumanAmp.value(mem, updateVal);
	}, {
	// Else:
		if (mem.at(\sinHealing) == false, {
			~setVisualsSinBarHealing.value(mem);
			mem.put(\sinHealing, true);
		});
		~updateSin.value(mem, updateVal);
	});
};

~updateSinAmp = {
    // Function that updates the anti-human sin wave amplitude.
	arg mem, updateVal;
	// update sin amplitude value
	mem.put(\sinAmpVal, mem.at(\sinAmpVal) + updateVal);
	// update sin
	mem.at(\sin).do({
		arg item, i;
		item.set(\amp, mem.at(\sinAmpVal));
	});
};

~updateSinLFOPhase = {
	// Function that updates the phase of the LFO on the anti-human sin wave.
	arg mem, updateVal;
	// update sin LFO Phase
	mem.put(\sinLFOPhase, (mem.at(\sinLFOPhase) - updateVal));
	// If less than 0 set to 0
	if (mem.at(\sinLFOPhase) <= 0, {
		mem.put(\sinLFOPhase, 0);
	});
	// Set sin LFO Phase
	mem.at(\sin).do({
		arg item, i;
		item.set(\lfoPhase, (i * mem.at(\sinLFOPhase)));
	});

};

~updateSinLFOFreq = {
	// Function that updates the frequency of the LFO on the sin-human sin wave
	arg mem, updateVal;
	mem.put(\sinLFOFreq, (mem.at(\sinLFOFreq) - updateVal));
	// If less than 0 set to 0
	if (mem.at(\sinLFOFreq) <= 0, {
		mem.put(\sinLFOFreq, 0);
	});
	mem.at(\sin).do({
		arg item, i;
		item.set(\sinLFOFreq, (i * mem.at(\sinLFOFreq)));
	});

};

~updateSin = {
	/*
	Function with logic on the sin waves:
	~the sin waves start as off.
	~When reach peak, antiHumanInstrument falls off
	~when antiHumanInstrument is out entirely, Sin LFOs narrow down to pure sin wave
	~when only pure sin waves, 5 minute gliss to single pitch.
	*/
	arg mem, updateVal;
	if (mem.at(\sinMaxed), {
		// Set audience to defeated
		if (mem.at(\audienceDefeated) == false, {
			"audience defeated".postln;
			~sendVisualsAudienceDefeated.value(mem);
			mem.put(\audienceDefeated, true);
		});
		// If antiHuman Turned off and audience defeated
		if (mem.at(\audienceDefeated) && (mem.at(\antiHumanAmpVal) <= 0), {
			// if pure sin tones
			if (mem.at(\pureSins), {
				// initiate end sequence
				if (mem.at(\glissActivated) != true, {
					mem.at(\sin).do({arg item, i; item.set(\freq, 10000); });
				});
			}, {
				// Check if Phase is <= 0
				if ((mem.at(\sinLFOPhase) <= 0) && (mem.at(\sinLFOFreq) <= 0), {
					mem.put(\pureSins, true);
				});
				~updateSinLFOPhase.value(mem, updateVal);
				~updateSinLFOFreq.value(mem, updateVal.linlin(0, 0.1, 0, 0.01));
			});
		}, {
			// Turn down anti human amp
			~updateAntiHumanAmp.value(mem, -0.1);
		});
	}, {
		~updateSinAmp.value(mem, updateVal);
		if (mem.at(\sinAmpVal) >= mem.at(\sinMax), {
			if ((mem.at(\sinMaxed) == false), {
				mem.at(\antiHumanBaseNoise).do({arg item, i; item.set(\gate, 0) });
			});
			mem.put(\sinMaxed, true);
		});
	});

};


~updateAntiHumanAmp = {
	// Function with logic to update the antiHumanInstrument's amplitude.
	arg mem, updateVal;
	// update Anti Human amplitude value
	mem.put(\antiHumanAmpVal, mem.at(\antiHumanAmpVal) + updateVal);

	// If less than 0 set to 0
	if (mem.at(\antiHumanAmpVal) <= 0, {
		mem.put(\antiHumanAmpVal, 0);
	});

	// If greater than 1, set to 1
	if (mem.at(\antiHumanAmpVal) >= 1, {
		mem.put(\antiHumanAmpVal, 1);
	});

	// update values in anti-human instruments
	mem.at(\antiHumanInst).do({
		arg item, i;
		item.set(\amp, mem.at(\antiHumanAmpVal));
	});

	mem.at(\antiHumanBaseNoise).do({
		arg item, i;
		item.set(\amp, mem.at(\antiHumanAmpVal));
	});


};

~respond = {
    // Function that builds a granulator or playback of some creepy sounds in response to an attack.
	arg mem, instrument, buffer, timeToFreeInst;
	var synth;
	if (instrument == \granulator, {
		synth = Synth(\granulator, [\buf, buffer, \dur, 10, \baseDur, 2, \amp, mem.at(\antiHumanAmpVal) / 2, \density, 23, \rateRand, 0.1, \durRand, 0.1, \rate, 3, \gate, 1]);
		SystemClock.sched(timeToFreeInst, { synth.set(\gate, 0); mem.put(\antiHumanResponding, false); });
	}, {
		synth = Synth(\playback, [\buf, buffer, \amp, mem.at(\antiHumanAmpVal), \pos, 1.rand2]);
	});

	instrument;
};

~selectInstrument = {
	// Randomly select and instrument from the instrument array and returns it.
	arg instArray;
	instArray.choose;
};

~calculateTimeToFreeInst = {
	// Calculates the time to free an instrument after it has been played.
	arg updateVal;
	updateVal.linlin(0.0, 1.0, 1.0, 4.0);
};

~changeAntiHumanInstrument = {
	arg mem, currentInstrument, newInstrument, amp;
	// if New Instrument is not the current instrument
		if ((currentInstrument.asSymbol != newInstrument.asSymbol), {
			// turn off current AntiHumanInstruments
			mem.at(\antiHumanInst).do({arg item, i; item.set(\gate, 0);});
			// change current AntiHumanInstrument to new Instrument
			mem.put(\currentAntiHumanInstrument, newInstrument);
			// turn on new Anti Human Instrument
			mem.put(\antiHumanInst, ~buildAntiHumanInstrumentArray.value(newInstrument, amp));
		});

	// else pass
};

~buildAntiHumanInstrumentArray = {
	arg instrument, amp;
	var antiHumanInstrumentArray;

	// If instrument selected is bitCrush, fill array of synths with updated new Instrument Values
	if ((instrument == \bitCrush), {
		antiHumanInstrumentArray = Array.fill(4, {arg i; Synth(instrument, [\x0, 0, \y0, 1+(i*0.2), \amp, amp, \maxFreqAdd, 1000+(1000*i), \pos, 1.0.rand2, \gate, 1])});
	});

	if ((instrument == \gendy), {
		antiHumanInstrumentArray = Array.fill(4, {arg i; Synth(instrument, [\minFreq, (76+(i*5.23)).midicps, \maxFreq, (98+(i*14.23)), \pos, 1.0.rand2, \amp, amp])});
	});

	if ((instrument == \standardNNoise), {
		antiHumanInstrumentArray = Array.fill(4, {arg i; Synth(instrument, [\out, 0, \amp, amp, \octave, i+1, \pos, 1.0.rand2, \gate, 1])});
	});

	if ((instrument == \sin), {
		antiHumanInstrumentArray = Array.fill(4, {arg i; Synth(instrument, [\freq, (96+(i*0.25)).midicps, \sinLFOFreq, 0.1333 + (i * 0.123.rand2), \lfoPhase, (0.22333 + (i * 0.2333.rand2)),\pos, 1.0.rand2, \amp, amp])});
	});


	antiHumanInstrumentArray;
};

~buildResponseBuffers = {
	arg folderPath;
	var array, path;
	path = PathName.new(folderPath);
	array = List.new();
	path.filesDo({ arg file;
		if (file.fullPath.endsWith(".wav"), {
			array.add(Buffer.readChannel(s, file.fullPath, channels: [0]));
		});

	});
	array;
};

~sendHeal2Visuals = {
	arg mem, updateVal;
	if (mem.at(\audienceDefeated) == false) {
		mem.at(\visuals_netaddress).sendMsg("/heal", updateVal);
	};
};

~sendChangeVisuals = {
	arg mem, index;
	mem.at(\visuals_netaddress).sendMsg("/change_visuals", index);
};

~sendVisualsStartMain = {
	arg mem;
	mem.at(\visuals_netaddress).sendMsg("/end_introduction");
};

~sendVisualsAudienceWon = {
	arg mem;
	mem.at(\visuals_netaddress).sendMsg("/audience_won");
};

~sendVisualsAudienceDefeated = {
	arg mem;
	mem.at(\visuals_netaddress).sendMsg("/audience_defeated");
};

~sendVisualsIntroWhite = {
	arg mem, bool;
	mem.at(\visuals_netaddress).sendMsg("/introWhite", bool);
};

~sendVisualsReadyToStart = {
	arg mem;
	mem.at(\visuals_netaddress).sendMsg("/readyToStart");
};

~setVisualsSinBarHealing = {
	arg mem;
	mem.at(\visuals_netaddress).sendMsg("/sinBarHealing");
};

~main = {
	if(~gm.at(\introduction), {
		"running introduction".postln;
		~sendVisualsReadyToStart.value(~gm);
		~gm.at(\antiHumanInst).do({arg item, i; item.set(\amp, 0.5)});
		~gm.at(\antiHumanBaseNoise).do({arg item, i; item.set(\amp, 1)});
		~introduction.reset;
		~introduction.play();
	}, {
		"running main".postln;
		~mainRoutine.reset;
		~sendVisualsStartMain.value(~gm);
		~mainRoutine.play();
		~introduction.stop();
	});
};

)



// ~changeAntiHumanInstrument.value(~gm, ~gm.at(\currentAntiHumanInstrument), \standardNNoise, []);
//
// ~respond.value(\bitCrush, 2.2);
//
// ~gm.at(\currentAntiHumanInstrument);
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
