(
~buildWaveTables = {
	arg numTables=4, tableSize=1024;
	var array;
	array = Array.fill(numTables, {
		var numSegs = rrand(4, 20);
		Env(
			levels: [0] ++ (({rrand(0.0, 1.0)}!(numSegs-1)) * [1, -1]).scramble ++ [0],
			times: {exprand(1, 20)}!numSegs,
			curve: {rrand(-20,20)}!numSegs
		).asSignal(tableSize).asWavetable;
	});
	array;
};

~allocConsecutiveBuffers = {
	arg numBuffers, bufSize;
	var buffers;
	buffers = Buffer.allocConsecutive(numBuffers, s, bufSize);
	buffers;
};

~loadWaveTablesToBuffers = {
	arg buffers, waveTables;
	buffers.do({
		arg buf, i;
		buf.loadCollection(waveTables[i]);
	});
	buffers;
};

~makeWtBuffers = {
	arg numBuffers=4, tableSize=1024;
	var waveTables, buffers;
	waveTables = ~buildWaveTables.value(numBuffers, tableSize);
	buffers = ~allocConsecutiveBuffers.value(numBuffers, tableSize*2);
	buffers = ~loadWaveTablesToBuffers.value(buffers, waveTables);
	buffers;
};

~makeWtBuffers.value()
)