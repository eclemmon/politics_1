public class Color {
  private int r;
  private int g;
  private int b;
  
  public Color(int r, int g, int b) {
    this.r = r;
    this.g = g;
    this.b = b;
  };
  
  public void fill_color() {
    fill(r, g, b);
  };
  
  public void stroke_color() {
    stroke(r, g, b);
  };
  
  public void fill_color_with_alpha(int alpha) {
    fill(r, g, b, alpha);
  };
  
  public void stroke_color_with_alpha(int alpha) {
    stroke(r, g, b, alpha);
  };
  
  public void background_color() {
    background(r, g, b);
  };
 
  public int get_r() {
    return this.r;
  }
  
  public int get_g() {
    return this.g;
  };
  
  public int get_b() {
    return this.b;
  };
  
  public void set_r(int r) {
    this.r = r;
  };
  
  public void set_g(int g) {
    this.g = g;
  };
  
  public void set_b(int b) {
    this.b = b;
  };
  
  @Override
  public String toString() {
    return "("+this.r +", "+this.g+", "+this.b+")";
  }
  
}
