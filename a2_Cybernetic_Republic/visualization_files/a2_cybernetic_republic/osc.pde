void mousePressed() {
  OscMessage myMessage = new OscMessage("/end_section");
  oscP5.send(myMessage, receiver);
  //println(messageList);
}


void oscEvent(OscMessage m) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.\n");
  print("addrpattern: " + m.addrPattern());
  println(" typetag: " + m.typetag());
  
  
  if (m.addrPattern().equals("/count")) {
    countText.setMessageAndTextWidth(m.get(0).toString());
  };
  
  if (m.addrPattern().equals("/vote_tally")) {
    // kill me but there are only four arguments anyways. Why can't OSCp5 iterate over an OSCMessage argument's? Or am I missing something.
    for (int i = 0; i <= 3; i++) {
      voteTextQueue.add(m.get(i).toString());
    };
  };
  
  if (m.addrPattern().equals("/update_vote_tally")) {
    for (int i=0; i <= 3; i++) {
       voteTextQueue.update_vote_text(i, m.get(i).toString());
    };
  };
  
  if (m.addrPattern().equals("/end_section")) {
    voteTextQueue.set_votes_exiting();
    sectionTextQueue.set_votes_exiting();
    voteTextQueue.reset();
    sectionTextQueue.reset();
  };
  
  if (m.addrPattern().equals("/selected_vote")) {
    voteTextQueue.set_selected_vote(m.get(0).intValue());
  };
  
  if (m.addrPattern().equals("/rhythm_section")) {
    rhythmSectionBackgroundGraphic.update_background();
  };
  
  if (m.addrPattern().equals("/middle_voice")) {
    middleVoicesBackgroundGraphic.update_background();
  };
  
  if (m.addrPattern().equals("/melody")) {
    melodyBackgroundGraphic.update_background();
  };
  
  if (m.addrPattern().equals("/bass")) {
    bassBackgroundGraphic.update_background();
  };
  
  if (m.addrPattern().equals("/start")) {
    started = true;
    preroll = false;
  };
  
  if (m.addrPattern().equals("/end")) {
    ended = true;
  };
  
  if (m.addrPattern().equals("/start_introduction")) {
    introduction = true;
  };
  
  if (m.addrPattern().equals("/end_introduction")) {
    introduction = false;
  };
  
  if (m.addrPattern().equals("/section_title")) {
     sectionTextQueue.add(m.get(0).toString());
  };
  

}
