import oscP5.*;
import netP5.*;
OscP5 oscP5;
NetAddress receiver;
String count;
boolean started;
boolean ended;
boolean introduction;
boolean preroll;
float introductionTextStartingXPos;
float imageAlpha;
Color textColor;
CountText countText;
VoteTextQueue voteTextQueue;
VoteTextQueue sectionTextQueue;
Text twitter;
Text phone;
Text introductionText;
Text prerollText;
ColorScheme rhythmColorScheme;
ColorScheme melodyColorScheme;
ColorScheme bassColorScheme;
ColorScheme middleVoicesColorScheme;
BackgroundGraphic rhythmSectionBackgroundGraphic;
BackgroundGraphic melodyBackgroundGraphic;
BackgroundGraphic bassBackgroundGraphic;
BackgroundGraphic middleVoicesBackgroundGraphic;
PImage qrCode;

void setup() {
  //fullScreen(1, P2D);
  size(1280, 720, P2D);
  frameRate(30);
  smooth();
  oscP5 = new OscP5(this, 12000);
  receiver = new NetAddress( "127.0.0.1", 12000);
  started = false;
  introduction = false;
  ended = false;
  preroll = true;
  textColor = new Color(255, 255, 255);
  rhythmColorScheme = new ColorScheme(188, 196, 219, 192, 169, 176, 120, 128, 181, 105, 135, 201);
  melodyColorScheme = new ColorScheme(34, 34, 59, 74, 78, 105, 154, 140, 152, 201, 173, 167);
  bassColorScheme = new ColorScheme(255, 123, 0, 255, 162, 0, 255, 195, 0, 255, 234, 0);
  middleVoicesColorScheme = new ColorScheme(40, 148, 127, 74, 167, 124, 132, 186, 99);
  rhythmSectionBackgroundGraphic = new BackgroundGraphic(rhythmColorScheme);
  melodyBackgroundGraphic = new BackgroundGraphic(melodyColorScheme);
  bassBackgroundGraphic = new BackgroundGraphic(bassColorScheme);
  middleVoicesBackgroundGraphic = new BackgroundGraphic(middleVoicesColorScheme);
  count = "";
  countText = new CountText(count, "FreeMonoBold.ttf", 70, textColor, width/2, 100);
  voteTextQueue = new VoteTextQueue(300, textColor);
  sectionTextQueue = new VoteTextQueue(200, new Color(0, 255, 0));
  twitter = new Text("Tweet: @InteractiveMus4", "FreeMonoBold.ttf", (height - 25), (width - 650), (height - 25));
  twitter.set_alpha(0);
  phone = new Text("SMS: (929) 334-3697 //", "FreeMonoBold.ttf", (height - 25), (width - 605 - 610), (height - 25));
  phone.set_alpha(0);
  prerollText = new Text("Starting soon:\nScan the QR code, or grab\nthe phone no. or twitter\nhandle below and get \nyour thumbs ready!", "FreeMonoBold.ttf", 120, 520, 120);
  prerollText.set_alpha(0);
  introductionText = new Text("Vote for this\n one here! -->", "FreeMonoBold.ttf", 240 + countText.get_text_height(), 100, 300);
  introductionText.set_alpha(0);
  qrCode = loadImage("qr-code.png");
  imageAlpha = 0;
}

void draw() {
  background(0);
  noStroke();
  if (preroll) {
    tint(255, imageAlpha);
    image(qrCode, 60, 60, 400, 400);
    imageAlpha += 7;
    if (imageAlpha > 255) {
      imageAlpha = 255;
    };
    twitter.fade_in();
    phone.fade_in();
    prerollText.fade_in();
  } else {
    textAlign(LEFT);
    prerollText.fade_out();
    tint(255, imageAlpha);
    image(qrCode, 60, 60, 400, 400);
    imageAlpha -= 7;
  };
  if (started) {
    rhythmSectionBackgroundGraphic.render();
    melodyBackgroundGraphic.render();
    bassBackgroundGraphic.render();
    middleVoicesBackgroundGraphic.render();
    countText.fade_in();
    sectionTextQueue.render_votes();
    voteTextQueue.render_votes();
    twitter.fade_in();
    phone.fade_in();
    if (introduction) {
      introductionTextStartingXPos = voteTextQueue.peek().text_width() + 50 + 300;
      introductionText.update_x(width * 5 / 6 - introductionTextStartingXPos);
      introductionText.fade_in();
    } else {
      introductionText.fade_out();
    };
  }
};
