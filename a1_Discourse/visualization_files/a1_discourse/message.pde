public class Message {
  private String message;
  private float y;
  private float x;
  private float current_alpha;
  private float speed;
  private PFont font;
  private float y_target;
  private float interpolation_rate;
  private int fontSize;
  private float x_target;
  private float maxWidth;
  private float textHeight;
  private boolean outOfBounds;
  private int rect_r;
  private int rect_g;
  private int rect_b;
  private int rect_alpha;

  public Message(String message, String font, int fontSize, float x, float y, float x_target, float maxWidth) {
    this.message = message;
    this.y = y;
    this.x = x;
    this.current_alpha = 255;
    this.speed = 30;
    this.fontSize = fontSize;
    this.font = createFont(font, this.fontSize);
    this.interpolation_rate = 0.01;
    this.x_target = x_target;
    this.maxWidth = maxWidth;
    this.textHeight = textHeight();
    this.y_target = height - this.textHeight - 100;
    this.outOfBounds = false;
    this.rect_r = floor(random(100, 255));
    this.rect_g = floor(random(100, 255));
    this.rect_b = floor(random(100, 255));
    this.rect_alpha = floor(random(100, 200));
  }

  public float x() {
    return this.x;
  }

  public void update_x(float amount) {
    this.x = amount;
  }
  
  public float y() {
    return this.y;
  }

  public void update_y(float amount) {
    this.y = amount;
  }
  
  public float get_textHeight() {
    return this.textHeight;
  };

  public String toString() {
    return this.message;
  }
  
  public boolean invisible() {
    return this.current_alpha <= 0;
  };
  
  public void update_alpha() {
    this.current_alpha = this.current_alpha - this.speed;
  };
  
  public void set_alpha(int i) {
    this.current_alpha = i;
  };
  
  public void interpolate_y() {
    if (abs((this.y_target - this.y)) < 1) {
      this.y = this.y_target;
    } else {
      this.y = (this.y_target - this.y) * this.interpolation_rate + this.y;
    };
  };
  
  public void interpolate_alpha() {
    if (abs((0 - this.current_alpha)) < 0.9) {
      this.current_alpha = 0;
    } else {
      this.current_alpha = (0 - this.current_alpha) * this.interpolation_rate + this.current_alpha;
    };
  };
  
  public float text_width() {
    textFont(this.font);
    return textWidth(this.toString());
  };
  
  public void move_y() {
    if (this.y - this.y_target < 1) {
      this.y = this.y_target;
    } else {
      this.y = this.y - this.speed;
    };
    
    if (this.y <= -this.textHeight) {
      this.set_out_of_bounds(true);
    };
  };
  
  public void set_y_target(float y_target) {
    this.y_target = y_target;
  };
  
  public float get_y_target() {
    return this.y_target;
  };
  
  public void render() {
    this.move_y();
    textFont(this.font);
    fill(this.rect_r, this.rect_g, this.rect_b, this.rect_alpha);
    rect(0, this.y(), width, this.textHeight);
    fill(33, 37, 41, this.current_alpha);
    text(this.toString(), this.x(), this.y(), this.maxWidth, this.textHeight);
  };
  
  public void set_out_of_bounds(Boolean bool) {
    this.outOfBounds = bool;
  };
  
  public boolean get_out_of_bounds() {
    return this.outOfBounds;
  };
  
  public float textHeight() {
    textFont(this.font);
    //StringList characters = new StringList();
    float w = 0;
    int i = 0;
    int lastSpace = 0;
    int numLines = 2;
    while (i < this.message.length()) {
      char c = this.message.charAt(i);
      w = w + textWidth(c);
      if (c == ' ') {
        lastSpace = i;
      };
      if (w > this.maxWidth) {
        numLines += 1;
        i = lastSpace;
        w = 0;
      } else {
        i += 1;
      };
    };
    return numLines * (textAscent() + textDescent());
  };
  
  public void fade_in() {
    if (this.current_alpha <= 255) {
      this.current_alpha += this.speed;
    };
    textFont(this.font);
    textSize(this.fontSize);
    fill(255, this.current_alpha);
    text(this.toString(), this.x(), this.y());
  };
  
  public void fade_out() {
    if (this.current_alpha >= 0) {
      this.current_alpha -= this.speed;
    };
    textFont(this.font);
    textSize(this.fontSize);
    fill(255, this.current_alpha);
    text(this.toString(), this.x(), this.y());
  };

}
