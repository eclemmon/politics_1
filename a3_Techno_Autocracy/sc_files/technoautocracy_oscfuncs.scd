(
~netaddress = NetAddr.new("127.0.0.1", 57120);
OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	~attack.value(~gm, args[1]);
	"######################################".postln;
}, '/attack');

OSCFunc({ |args|
	"######################################".postln;
	"OSCFUNC received the following values:".postln;
	args.postcs;
	~support.value(~gm, args[1]);
	"######################################".postln;
}, '/support');
)
