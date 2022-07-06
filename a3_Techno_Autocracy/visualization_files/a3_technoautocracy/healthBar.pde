public class HealthBar {
  private float max_health;
  private float min_health;
  private float health;
  private ColorScheme colorScheme;
  private int min_alpha;
  private int max_alpha;
  private int current_alpha;
  private int speed;
  private boolean increasing;
  private int y_placement;
  private float y_speed;
  private int min_y;
  private int max_y;
  private boolean y_increasing;
  private int y_speed_decrease;
  private int y_speed_test;
  private boolean fadeOut;
  private boolean sinBar;
  
  public HealthBar(float max_health, float min_health, float health, ColorScheme colorScheme, boolean sinBar) {
    this.max_health = max_health;
    this.min_health = min_health;
    this.health = health;
    // COLOR SCHEME MUST ONLY HAVE TWO COLORS
    this.colorScheme = colorScheme;
    this.min_alpha = 200;
    this.max_alpha = 255;
    this.speed = 3;
    this.increasing = true;
    this.current_alpha = 0;
    this.y_placement = 50;
    this.y_speed = 1;
    this.y_increasing = true;
    this.min_y = 40;
    this.max_y = 60;
    this.y_speed_decrease = 2;
    this.y_speed_test = 0;
    this.fadeOut = false;
    this.sinBar = sinBar;
  };
  
  public void set_health(float health) {
    this.health = health;
  };
  
  public float get_health() {
    return this.health;
  };
  
  public void set_fade_out(boolean fadeOut) {
    this.fadeOut = fadeOut;
  };
  
  public void render() {
    this.update_alpha();
    this.update_y_placement();
    float h = height - 100;
    float w = 100;
    strokeWeight(16);
    noFill();
    this.colorScheme.get(0).stroke_color_with_alpha(this.current_alpha);
    rect(50-8, this.y_placement-8, w+16, h+16);
    noStroke();
    if (!this.sinBar) {
      this.colorScheme.get(1).fill_color_with_alpha(this.current_alpha);
      rect(50, this.y_placement, w, h);
      fill(255, 0, 0, this.current_alpha);
    } else {
      fill(0, 255, 0, this.current_alpha);
    }
    rect(50, (height + this.y_placement - 100 - (h * (this.health / this.max_health))), w, h * (this.health / this.max_health));
    
  };
  
  public void update_health(float health) {
    this.health = this.health + health;
    if (this.health >= this.max_health) {
      this.health = this.max_health;
    }
    
    if (this.health <= this.min_health) {
      this.health = this.min_health;
    }
  };
  
  public void set_alpha(int alpha) {
    this.current_alpha = alpha;
  };
  
  public int get_alpha() {
    return this.current_alpha;
  };
  
  public boolean get_increasing() {
    return this.increasing;
  };
  
  public void set_increasing(boolean increasing) {
    this.increasing = increasing;
  };
  
  public void set_speed(int speed) {
    this.speed = speed;
  };
  
  public void set_y_placement(int y_placement) {
    this.y_placement = y_placement;
  };
  
  public void set_y_speed(int y_speed) {
    this.y_speed = y_speed;
  };
  
  public void set_min_alpha(int min_alpha) {
    this.min_alpha = min_alpha;
  };
  
  public void set_max_alpha(int max_alpha) {
    this.max_alpha = max_alpha;
  };
  
  public void update_alpha() {
    if (!this.fadeOut) {
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
    } else {
      this.increasing = false;
      if (this.current_alpha >= this.min_alpha) {
        this.current_alpha -= speed;
      };
    };
  };
  
  public void update_y_placement() {
    if (this.move_y_test()) {
      if (this.y_increasing) {
        this.y_placement += this.y_speed;
        if (this.y_placement >= this.max_y) {
          this.y_increasing = false;
        };
      } else {
        this.y_placement -= this.y_speed;
        if (this.y_placement <= this.min_y) {
          this.y_increasing = true;
        };
      };
    };
  };
  
  public boolean move_y_test() {
    this.y_speed_test += 1;
    if(this.y_speed_test >= this.y_speed_decrease) {
      this.y_speed_test = 0;
      return true;
    } else {
      return false;
    }
  };
};
