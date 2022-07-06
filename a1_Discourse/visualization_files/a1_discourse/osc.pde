void mousePressed() {
  OscMessage myMessage = new OscMessage("/hallo");
  myMessage.add("EM IPSUM LOREM IPSUM LOREM IPSUMLOREM IPSUM LOREM IPSUM LOREM IPSUM LOREM IPSUM LOREM IPSUM LOREM IPSUM END");
  oscP5.send(myMessage, receiver);
  //println(messageList);
}

void oscEvent(OscMessage m) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.\n");
  print("addrpattern: " + m.addrPattern());
  println(" typetag: " + m.typetag());
  String words = m.get(0).toString();
  float x = width/ random(5, 6);
  Message message = new Message(words, "FreeMonoBold.ttf", 70, 20, height, 0, width-40);
  messageQueue.add(message);
};
