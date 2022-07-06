public class StaticMessage {
  private String message;
  private float y;
  private float x;
  private float current_alpha;
  private float speed;
  private PFont font;
  private float y_target;
  private float interpolation_rate;
  private int fontSize;

  public StaticMessage(String message, String font, float y, float x, float y_target) {
    this.message = message;
    this.y = y;
    this.y_target = y_target;
    this.x = x;
    this.current_alpha = 255;
    this.speed = 7;
    this.fontSize = 40;
    this.font = createFont(font, 70);
    this.interpolation_rate = 0.01;
  }

  public float x() {
    return this.x;
  }

  public void update_x(float amount) {
    this.x = amount;
  }

  public void update_y(float amount) {
    this.y = amount;
  }

  public float y() {
    return this.y;
  }

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
  
  public void render() {
    this.interpolate_y();
    this.interpolate_alpha();
    textFont(this.font);
    fill(33, 37, 41, this.current_alpha);
    text(this.toString(), this.x(), this.y());
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
