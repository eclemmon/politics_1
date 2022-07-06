import oscP5.*;
import netP5.*;
OscP5 oscP5;
NetAddress receiver;
ColorScheme color_scheme;
ColorScheme hbColorScheme;
ColorScheme sbColorScheme;
HealthBar healthBar;
HealthBar sinBar;
AttackQueue attackQueue;
MessageQueue messageQueue;
ArrowQueue arrowQueue;
AudienceDefeated audienceDefeatedClass;
AudienceDefeated audienceWonClass;
Message twitter;
Message phone;
Overlay o1;
Overlay o2;
Overlay o3;
Overlay o4;
TextureRender textureRender;
ImageGlitch imageGlitch;
int glitch_texture;
boolean antiHumanHealing;
boolean introduction;
boolean audienceDefeated;
boolean audienceWon;
boolean introWhite;
boolean readyToStart;
boolean sinBarHealing;


void setup() {
  fullScreen(1, P2D);
  frameRate(30);
  smooth();
  glitch_texture = 0;
  readyToStart = false;
  introduction = true;
  introWhite = false;
  audienceDefeated = false;
  audienceWon = false;
  sinBarHealing = false;
  audienceDefeatedClass = new AudienceDefeated(60, 0);
  audienceWonClass = new AudienceDefeated(5, 255);
  color_scheme = new ColorScheme(248, 249, 250, 233, 236, 239, 33, 37, 41, 55, 6, 23, 208, 0, 0, 106, 4, 15, 255, 186, 8);
  hbColorScheme = new ColorScheme(54, 44, 40, 255, 134, 0);
  sbColorScheme = new ColorScheme(248, 249, 250, 255, 134, 0);
  healthBar = new HealthBar(100, 1, 50, hbColorScheme, false);
  sinBar = new HealthBar(100, 0, 0, sbColorScheme, true);
  twitter = new Message("Tweet: @InteractiveMus4", "FreeMonoBold.ttf", (height - 25), (width - 595), (height - 25));
  twitter.set_alpha(0);
  phone = new Message("SMS: (929) 334-3697 //", "FreeMonoBold.ttf", (height - 25), (width - 545 - 610), (height - 25));
  phone.set_alpha(0);
  o1 = new Overlay(89, 13, 34, 125, 75, 200, 25);
  o2 = new Overlay(33, 37, 41, 125, 75, 200, 20);
  o3 = new Overlay(69, 123, 157, 125, 75, 200, 15);
  o4 = new Overlay(255, 255, 252, 125, 75, 200, 10);
  Overlay[] overlays = {o1, o2, o3, o4};
  oscP5 = new OscP5(this, 12000);
  receiver = new NetAddress( "127.0.0.1", 12000);
  attackQueue = new AttackQueue();
  messageQueue = new MessageQueue();
  arrowQueue = new ArrowQueue();
  imageGlitch = new ImageGlitch("/Users/ericlemmon/Documents/PhD/PhD_Project_v2/Resources/a3_technoautocracy_images", 30);
  textureRender = new TextureRender(color_scheme, overlays, imageGlitch, healthBar);
  
}

void draw() {
  background(0);
  noStroke();
  if (readyToStart) {
    if (introduction) {
      if(!introWhite) {
        textureRender.textureRender(glitch_texture % 4);
      } else {
        fill(255);
        rect(0, 0, width, height);
      };
    };
    
    if(!introduction && !audienceDefeated && !audienceWon) {
      textureRender.textureRender(glitch_texture % 4);
      healthBar.render();
      sinBar.render();
      twitter.fade_in();
      phone.fade_in();
      attackQueue.render_attacks();
      messageQueue.render_messages();
      arrowQueue.render_arrows();
    };
    
    if (!introduction && audienceDefeated) {
      textureRender.textureRender(glitch_texture % 4);
      audienceDefeatedClass.render();
      healthBar.render();
      sinBar.render();
      twitter.fade_out();
      phone.fade_out();
    };
    
    if (!introduction && audienceWon) {
      textureRender.textureRender(glitch_texture % 4);
      audienceWonClass.render();
      healthBar.render();
      sinBar.render();
      twitter.fade_out();
      phone.fade_out();
    };
  };
}
