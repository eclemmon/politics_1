public class Arrow {
  private float y;
  private float x;
  private float current_alpha;
  private float speed;
  private float y_target;
  private float interpolation_rate;
  private float w;
  private float h;
  private PImage img;

  public Arrow(String img_path, float y, float x, float y_target, float w, float h) {
    this.y = y;
    this.y_target = y_target;
    this.x = x;
    this.w = w;
    this.h = h;
    this.current_alpha = 255;
    this.speed = 7;
    this.interpolation_rate = 0.3;
    this.img = loadImage(img_path);
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
  
  public boolean invisible() {
    return this.current_alpha <= 0;
  };
  
  public void update_alpha() {
    this.current_alpha = this.current_alpha - this.speed;
  };
  
  public void interpolate_y() {
    if (abs((this.y_target - this.y)) < 0) {
      this.y = this.y_target;
    } else {
      this.y = (this.y_target - this.y) * this.interpolation_rate + this.y;
    };
  };
  
  public void interpolate_alpha() {
    if (abs((0 - this.current_alpha)) < 0.7) {
      this.current_alpha = 0;
    } else {
      this.current_alpha = (0 - this.current_alpha) * this.interpolation_rate + this.current_alpha;
    };
  };
  
  public void render() {
    this.interpolate_y();
    this.interpolate_alpha();
    tint(255, this.current_alpha);
    image(this.img, this.x, this.y, this.w, this.h);
  };

}
