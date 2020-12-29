s = Server.default.boot;
(
OSCFunc({|args|
	"OSCFUNC received the following values from message '/filter':".postln;
	args[1..].postln;
}, '/filter');
)