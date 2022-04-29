public class BackgroundGraphic {
  private int num = 100;
  private int range = 25;
  private float[] ax = new float[num];
  private float[] ay = new float[num];
  private boolean on;
  private ColorScheme colorScheme;
  private Color c;
  
  public BackgroundGraphic(ColorScheme colorScheme) {
    for(int i = 0; i < this.num; i++) {
      ax[i] = width / 2;
      ay[i] = height / 2;
    };
    this.on = false;
    this.colorScheme = colorScheme;
    this.c = this.colorScheme.choose();
  };
  
  public void update_background() {
    // Brownian motion algorithm
    for(int i = 1; i < num; i++) {
      this.ax[i-1] = this.ax[i];
      this.ay[i-1] = this.ay[i];
    };
    
    this.ax[num-1] += random(-range, range);
    this.ay[num-1] += random(-range, range);
    
    this.ax[num-1] = constrain(ax[num-1], 0, width);
    this.ay[num-1] = constrain(ay[num-1], 0, height);
  };
  
  public void render() {
    for(int i = 1; i < num; i++) {
      float alpha = float(i) / this.num * 204.0 + 51;
      float strokeWeight = float(i) / this.num * 3 + 2;
      strokeWeight(strokeWeight);
      stroke(this.c.get_r(), this.c.get_g(), this.c.get_b(), alpha);
      line(ax[i-1], ay[i-1], ax[i], ay[i]);
    };
  };
  
  public void set_on_off(boolean on_off) {
    this.on = on_off;
  };
  
};
