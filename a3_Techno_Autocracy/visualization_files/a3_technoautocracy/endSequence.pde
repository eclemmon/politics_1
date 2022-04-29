public class AudienceDefeated {
  private float alpha;
  private float fadeDuration;
  private float currentTextAlpha;
  private int max_alpha;
  private int min_alpha;
  private int clr;
  private boolean flashTexture;
  private boolean increasing;
  
  public AudienceDefeated(float fadeDuration, int clr) {
    this.alpha = 0;
    this.currentTextAlpha = 0;
    this.min_alpha = 100;
    this.max_alpha = 255;
    this.clr = clr;
    this.fadeDuration = fadeDuration * frameRate;
    this.flashTexture = false;
    this.increasing = true;
  };
  
  public void render() {
    fill(clr, this.alpha);
    rect(0, 0, width, height);
    if (this.alpha <= 255) {
      this.alpha += 255 / this.fadeDuration;
    }
  };
  
  public void update_text_alpha() {
    if (this.increasing) {
      this.currentTextAlpha += 255 / (this.fadeDuration * 2);
      if (this.currentTextAlpha >= this.max_alpha) {
        this.increasing = false;
      };
    } else {
     this.currentTextAlpha -= 255 / (this.fadeDuration * 2);
      if (this.currentTextAlpha <= this.min_alpha) {
        this.increasing = true;
      };
    };
  };
  
  
};
