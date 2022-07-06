public class FlashingText {
  private String message;
  private float y;
  private float x;
  private Color textColor;
  private Color rectColor;
  private PFont font;
  private int fontSize;
  private float textWidth;
  private boolean flashing;
  private int flashCount;
  
  public FlashingText(String message, String font, int fontSize, Color textColor, float x, float y) {
    this.message = message;
    this.y = y;
    this.x = x;
    this.textColor = textColor;
    this.rectColor = new Color(255-textColor.get_r(), 255-textColor.get_g(), 255-textColor.get_b());
    this.fontSize = fontSize;
    this.font = createFont(font, this.fontSize);
    this.textWidth = this.text_width();
    this.flashing = false;
    this.flashCount = 0;
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
  
  public void set_flashing(boolean flashing) {
    this.flashing = flashing;
  };
   
  public void render() {
    if (this.flashing) {
      this.flash();
    } else {
      this.rectColor.fill_color();
      textFont(this.font);
      this.rectColor.fill_color();
      rect(this.x-5-(this.textWidth/2), this.y + 15-(textAscent() + textDescent()), this.textWidth+10, textAscent() + textDescent());
      this.textColor.fill_color();
      textAlign(CENTER);
      text(this.toString(), this.x(), this.y());
    };
  };
  
  public void flash() {
    if (this.flashCount <= 19) {
      this.textColor.invert_color();
      this.rectColor.invert_color();
      this.rectColor.fill_color();
      textFont(this.font);
      this.rectColor.fill_color();
      rect(this.x-5-(this.textWidth/2), this.y + 15-(textAscent() + textDescent()), this.textWidth+10, (textAscent() + textDescent() + 5) * 6);
      this.textColor.fill_color();
      textAlign(CENTER);
      text(this.toString(), this.x(), this.y());
      this.flashCount += 1;
    } else {
      this.flashing = false;
      this.flashCount = 0;
    };
  };
  
  
};
