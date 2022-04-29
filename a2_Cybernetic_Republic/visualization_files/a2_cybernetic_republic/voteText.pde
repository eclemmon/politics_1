public class VoteText {
  private String message;
  private float y;
  private float x;
  private float distancePastCenter;
  private Color textColor;
  private PFont font;
  private int fontSize;
  private float textWidth;
  private boolean arrivedAtCenter;
  private boolean arrivedPastCenter;
  private boolean offScreenLeft;
  private boolean exiting;
  private boolean arrivedAtBottom;
  private boolean selectedVote;
  private float speed;

  public VoteText(String message, String font, int fontSize, Color textColor, float x, float y) {
    this.message = message;
    this.y = y;
    this.x = x;
    this.distancePastCenter = 30;
    this.textColor = textColor;
    this.fontSize = fontSize;
    this.font = createFont(font, this.fontSize);
    this.textWidth = this.text_width();
    this.arrivedAtCenter = false;
    this.arrivedPastCenter = false;
    this.offScreenLeft = false;
    this.exiting = false;
    this.arrivedAtBottom = false;
    this.selectedVote = false;
    this.speed = 15;
  };
  
  public float x() {
    return this.x;
  };
  
  public float y() {
    return this.y;
  };
  
  public void set_x(float x) {
    this.x = x;
  };
  
  public void set_y(float y) {
    this.y = y;
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
  
  public float text_height() {
    return textAscent() + textDescent();
  };
  
  public void render() {
    if (!this.arrivedAtCenter && this.arrivedPastCenter) {
      this.goToCenter();
    }
    if (!this.arrivedAtCenter && !this.arrivedPastCenter) {
      this.goPastCenter();
    };
    if (this.exiting) {
      this.goOffScreen();
    };
    if (this.selectedVote) {
      this.set_selected_color();
    };
    textFont(this.font);
    this.textColor.fill_color();
    textAlign(RIGHT);
    text(this.toString(), this.x(), this.y());
  }
  
  public void goPastCenter() {
    if (this.x() <= width * 5 / 6 - this.distancePastCenter) {
      this.arrivedPastCenter = true;
      this.set_x(width * 5 / 6 - this.distancePastCenter);
    } else {
      if (this.x() <= width) {
        if (this.speed > 3) {
          this.accelerate_after_n_frames(20, -2);
        } else {
          this.speed = 3;
        };
      };
      this.x -= this.speed;
    };
  };
  
  public void goToCenter() {
    if (this.x() >= width * 5 / 6) {
      this.arrivedAtCenter = true;
      this.set_x(width * 5 / 6);
    } else {
      this.x += 1;
    };
  };

  public void goOffScreen() {
    if (this.x() < -this.textWidth) {
      this.offScreenLeft = true;
      this.exiting = false;
    } else {
      this.accelerate_after_n_frames(15, 1);
      this.x -= this.speed;
    };
  };
  
  public void goToBottom() {
    if (!this.arrivedAtBottom) {
      this.accelerate_after_n_frames(15, 1);
      this.y += this.speed;
      if (this.y >= height * 5 / 6) {
          this.y = height * 5 / 6;
          this.arrivedAtBottom = true;
      };
    };
  };
  
  public void accelerate(int speed) {
    this.speed += speed;
  };
  
  public void accelerate_after_n_frames(int n_frames, int speed) {
    if (frameCount % n_frames == 0) {
      this.accelerate(speed);
    }
  };
  
  public void set_exiting(boolean exiting) {
    this.exiting = exiting;
  };
  
  public void set_selected_vote(boolean selectedVote) {
    this.selectedVote = selectedVote;
  };
  
  public boolean selected_vote() {
    return this.selected_vote();
  };
  
  public boolean offScreen() {
    return this.offScreenLeft;
  };

  public void set_selected_color() {
    this.textColor = new Color(255, 0, 0);
  };
};
