public class Noise {
  private ColorScheme colorScheme;
  private int current_alpha;
  private int min_alpha;
  private int max_alpha;
  private float speed;
  private boolean increasing;
  
  public Noise(ColorScheme colorScheme, int current_alpha, int min_alpha, int max_alpha, float speed) {
    this.colorScheme = colorScheme;
    this.current_alpha = current_alpha;
    this.min_alpha = min_alpha;
    this.max_alpha = max_alpha;
    this.speed = speed;
    this.increasing = true;
  };
  
  public void render() {
    this.update_alpha();
    for(int x = 0; x < width; x++) {
      for (int y = 0; y < height; y++) {
        Color clr;
        clr = this.colorScheme.choose();
        clr.fill_color_with_alpha(this.current_alpha);
        rect(x, y, 1, 1);
      };
    };
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
