import java.util.HashMap;

public class TextureRender {
  private ColorScheme colorScheme1;
  private Overlay[] overlays;
  private ImageGlitch imageGlitch;
  private HealthBar healthBar;
  
  public TextureRender(ColorScheme colorScheme1, Overlay[] overlays, ImageGlitch imageGlitch, HealthBar healthBar) {
    this.colorScheme1 = colorScheme1;
    this.imageGlitch = imageGlitch;
    this.overlays = overlays;
    this.healthBar = healthBar;
  };
  
  public void textureRender(int index) {
    run_image_glitch(index);
  };
  
  public void run_flash(int index) {
    flash(this.colorScheme1);
    this.get_overlay(index).render();
  };
  
  public void run_shapes(int index) {
    generateShapes(4);
    noStroke();
    this.get_overlay(index).render();
  }; 
  
  public void run_image_glitch(int index) {
    this.imageGlitch.set_chanceToChange(random(30, 100));
    this.imageGlitch.render();
    this.get_overlay(index).render();
  };
  
  public float map_health_bar_to_alpha() {
    return healthBar.get_health() / 100 * 255;
  };
  
  public Overlay get_overlay(int index) {
    return this.overlays[index];
  };
  
};
