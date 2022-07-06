public class CountText {
  private String message;
  private float y;
  private float x;
  private Color textColor;
  private PFont font;
  private int fontSize;
  private float textWidth;
  private float current_alpha;
  private float speed;

  public CountText(String message, String font, int fontSize, Color textColor, float x, float y) {
    this.message = message;
    this.y = y;
    this.x = x;
    this.textColor = textColor;
    this.fontSize = fontSize;
    this.font = createFont(font, this.fontSize);
    this.textWidth = this.text_width();
    this.current_alpha = 0;
    this.speed = 8;
  };
  
  public float x() {
    return this.x;
  };
  
  public float y() {
    return this.y;
  };
  
  public String toString() {
    return this.message;
  };
  
  public void setMessage(String message) {
    this.message = message;
  };
  
  public void setMessageAndTextWidth(String message) {
    this.message = message;
    this.textWidth = this.text_width();
  };
  
  public float text_width() {
    textFont(this.font);
    return textWidth(this.toString());
  };
  
  public void render() {
    textFont(this.font);
    this.textColor.fill_color();
    textAlign(CENTER);
    text(this.toString(), this.x(), this.y());
  }
  
  public float get_text_height() {
    return textAscent() + textDescent();
  };
  
  public void fade_in() {
    if (this.current_alpha <= 255) {
      this.current_alpha += this.speed;
    };
    textFont(this.font);
    textSize(this.fontSize);
    textAlign(CENTER);
    fill(255, this.current_alpha);
    text(this.toString(), this.x(), this.y());
  };
  
  public void fade_out() {
    if (this.current_alpha >= 0) {
      this.current_alpha -= this.speed;
    };
    textFont(this.font);
    textSize(this.fontSize);
    textAlign(CENTER);
    fill(255, this.current_alpha);
    text(this.toString(), this.x(), this.y());
  };
};
