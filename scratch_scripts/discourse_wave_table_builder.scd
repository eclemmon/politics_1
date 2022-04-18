(
var buffers;
s=Server.default.boot;
~load_wavetable_buffers = {
	arg path, server;
	var folder, buffers;
	folder = PathName(path);
	buffers = folder.files.collect({
		arg file;
		var buffer, temp;
		buffer = Buffer.read(server, file.fullPath);
		temp = buffer.loadToFloatArray( action: { arg array; a = array;});
		temp.plot;
	});

};

buffers = ~load_wavetable_buffers.value("/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Resources/wavetables/", s);
buffers[0].postln;
Synth(\wavetable, [\out, 0, \buf, buffers[0], \numBufs, 2, \freq, 440, \amp, 1, \gate, 1, \dur, 10]);

)