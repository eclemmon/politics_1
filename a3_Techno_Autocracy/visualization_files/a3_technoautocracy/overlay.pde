public class Overlay {
  private Color clr;
  private int current_alpha;
  private int min_alpha;
  private int max_alpha;
  private float speed;
  private boolean increasing;
  
  public Overlay(int r, int g, int b, int current_alpha, int min_alpha, int max_alpha, float speed) {
    this.clr = new Color(r, b, g);
    this.current_alpha = current_alpha;
    this.min_alpha = min_alpha;
    this.max_alpha = max_alpha;
    this.speed = speed;
    this.increasing = true;
  };
  
  public void render() {
    this.update_alpha();
    this.clr.fill_color_with_alpha(this.current_alpha);
    rect(0, 0, width, height);
  };
  
  public void set_alpha(int alpha) {
    this.current_alpha = alpha;
  };
  
  public void set_speed(float speed) {
    this.speed = speed;
  };
  
  public void set_min_alpha(int min_alpha) {
    this.min_alpha = min_alpha;
  };
  
  public void set_max_alpha(int max_alpha) {
    this.max_alpha = max_alpha;
  };
  
  public void update_alpha() {
    if (this.increasing) {
      this.current_alpha += speed;
      if (this.current_alpha >= this.max_alpha) {
        this.increasing = false;
      };
    } else {
      this.current_alpha -= speed;
      if (this.current_alpha <= this.min_alpha) {
        this.increasing = true;
      };
    };
  };
  
  
  
};
