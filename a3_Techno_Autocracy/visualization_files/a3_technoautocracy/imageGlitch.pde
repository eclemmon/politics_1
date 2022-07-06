import java.io.File;
import java.util.ArrayList;

public class ImageGlitch {
  ArrayList<PImage> images;
  float chanceToChange;
  PImage currentImage;
  
  public ImageGlitch(String filePath, float chanceToChange) {
    File dir = new File(filePath);
    File[] files = dir.listFiles();
    this.images = new ArrayList<>();
    this.chanceToChange = chanceToChange / 100 * frameRate;

    
    for (File file: files) {
      String path = file.getAbsolutePath();
      if (path.endsWith(".png")) {
        PImage img = loadImage(path);
        img.resize(width, height);
        this.images.add(img);
      };
    };
    
    this.currentImage = this.get_random_image();
  };
  
  public PImage get_random_image() {
    return this.images.get(int(random(images.size())));
  }
  
  public void set_chanceToChange(float chanceToChange) {
    this.chanceToChange = chanceToChange / 100 * frameRate;
  };
  
  public void render() {
    float select = random(100);
    if (select <= this.chanceToChange) {
      this.currentImage = this.get_random_image();
      tint(255, 255);
      image(this.currentImage, 0, 0);
    } else {
      tint(255, 255);
      image(this.currentImage, 0, 0);
    };

  };
  
};
