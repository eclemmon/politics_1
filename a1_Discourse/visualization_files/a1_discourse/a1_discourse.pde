import com.jogamp.opengl.GLProfile;
{
  GLProfile.initSingleton();
}
import oscP5.*;
import netP5.*;
import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;
import java.util.Iterator;

OscP5 oscP5;
NetAddress receiver;
MessageQueue messageQueue;
Color backgroundColor;
Color waveColor;
BackgroundWave backgroundWave;
StaticMessage twitter;
StaticMessage phone;
Boolean scored;

void setup() {
  size(1280, 720, P2D);
  frameRate(30);
  smooth();
  scored = false;
  backgroundColor = new Color(124, 169, 130);
  waveColor = new Color(5, 59, 6);
  oscP5 = new OscP5(this, 12000);
  receiver = new NetAddress( "127.0.0.1", 12000);
  messageQueue = new MessageQueue();
  backgroundWave = new BackgroundWave(backgroundColor, waveColor, messageQueue);

  // Check if scored version of piece
  if (!scored) {
    twitter = new StaticMessage("Tweet: @InteractiveMus4", "FreeMonoBold.ttf", (height - 25), (width - 595), (height - 25));
    twitter.set_alpha(0);
    phone = new StaticMessage("SMS: +1 (929) 334-3697 //", "FreeMonoBold.ttf", (height - 25), (width - 545 - 675), (height - 25));
    phone.set_alpha(0);
  };
};

void draw() {
  backgroundWave.render();
  noStroke();

  // check if scored version of piece
  if (!scored) {
    twitter.fade_in();
    phone.fade_in();
  };
};
