void mousePressed() {
  OscMessage myMessage = new OscMessage("/support");
  myMessage.add("EricCLemmon");
  myMessage.add(1.224);
  oscP5.send(myMessage, receiver);
  //println(messageList);
}

String[] attackMessages = {" attacked \nthe despot for ",  " raged against \nthe machine for ",  " threw their body \non the gears for ",  " throttled the \ntechnocracy for ",  " fought the \npower for "};
String[] supportMessages = {" licked \na boot for ", " \ncollaborated against \nthe audience \nfor ", " rode a \ntank for ", " hates the \naudience this \nmuch: ", " wished this \nmuch ill on \nyou all: "};

void oscEvent(OscMessage m) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.\n");
  print("addrpattern: " + m.addrPattern());
  println(" typetag: " + m.typetag());
  
  // If address pattern is attack
  if (m.addrPattern().equals("/attack")) {
    // Make Message
    String attackMessage = attackMessages[int(random(attackMessages.length))];
    String words = m.get(0).toString() + attackMessage + String.valueOf(m.get(1).floatValue()) + "!!";
    // Add attack flash
    Attack attack = new Attack();
    attackQueue.add(attack);
    // Randomize Message location a little
    float x = width / random(5, 6);
    // Add message to render queue
    Message message = new Message(words, "FreeMonoBold.ttf", height/5*3, x, height/8 * 7);
    messageQueue.add(message);
    // Add down arrow to render queue
    Arrow arrow = new Arrow("down_arrow.png", height/5*3-35, x + message.text_width(), height/8*7-35, 80, 80);
    arrowQueue.add(arrow);
    // Update health bar
    if (sinBarHealing) {
      sinBar.update_health(m.get(1).floatValue() * 10);
    } else {
      healthBar.update_health(m.get(1).floatValue() * 10);
    }
    
  }
  
  if (m.addrPattern().equals("/support")) {
    glitch_texture += 1;
    glitch_texture = glitch_texture % 3;
    // Make Message
    String supportMessage = supportMessages[int(random(supportMessages.length))];
    String words = m.get(0).toString() + supportMessage + String.valueOf(m.get(1).floatValue()) + "!!";
    // Randomize Message location a little
    float x = width / random(5, 6);
    // Add message to render queue
    Message message = new Message(words, "FreeMonoBold.ttf", height/5*2, x, height/8 * 1);
    messageQueue.add(message);
    // Add up arrow to render queue
    Arrow arrow = new Arrow("up_arrow.png", height/5*2-35, x + message.text_width(), height/8*1-35, 80, 80);
    arrowQueue.add(arrow);
    // Update health bars
    if (sinBarHealing) {
      sinBar.update_health(m.get(1).floatValue() * 10);
    } else {
      healthBar.update_health(m.get(1).floatValue() * 10);
    }
  };
  
  if (m.addrPattern().equals("/heal")) {
    // Update the health bar
    print(m.get(0).floatValue());
    if (sinBarHealing) {
      sinBar.update_health(m.get(0).floatValue());
    } else {
      healthBar.update_health(m.get(0).floatValue());
    };
    // Machine healed message
    //String healMessage = "The Machine \nhealed: " + String.valueOf(m.get(0).floatValue()) + "!";
    //Message message = new Message(healMessage, "FreeMonoBold.ttf", height/10*9, 100, height/9 * 8);
    //messageQueue.add(message);
    // Add up arrow to render queue
    Arrow arrow = new Arrow("up_arrow.png",  height/8 * 7, 50, height/8 * 6, 80, 80);
    arrowQueue.add(arrow);
    
  };
  
  if (m.addrPattern().equals("/change_visuals")) {
    glitch_texture = m.get(0).intValue();
  };
  
  if (m.addrPattern().equals("/end_introduction")) {
    introduction = false;
  };
  
  if (m.addrPattern().equals("/audience_won")) {
    audienceWon = true;
    healthBar.set_fade_out(true);
    healthBar.set_min_alpha(0);
    sinBar.set_fade_out(true);
    sinBar.set_min_alpha(0);
  };
  
  if (m.addrPattern().equals("/audience_defeated")) {
    audienceDefeated = true;
    healthBar.set_fade_out(true);
    healthBar.set_min_alpha(0);
    sinBar.set_fade_out(true);
    sinBar.set_min_alpha(0);
  };
  
  if (m.addrPattern().equals("/introWhite")) {
    if (m.get(0).intValue() == 1) {
      introWhite = true;
      print(m.get(0).intValue());
    } else {
      introWhite = false;
      print(m.get(0).intValue());
    };
  };
  
  if (m.addrPattern().equals("/readyToStart")) {
    readyToStart = true;
  };
  
  if (m.addrPattern().equals("/sinBarHealing")) {
    sinBarHealing = true;
    sinBar.set_alpha(healthBar.get_alpha());
    sinBar.set_increasing(healthBar.get_increasing());
  };
  

}
