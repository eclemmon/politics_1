import java.util.ArrayList;
import java.util.Random;

public class ColorScheme {
  private ArrayList<Color> colors;
  private Random random_method;
  
  public ColorScheme(int... args) {
    // initialize color array list
    this.colors = new ArrayList<Color>();
    // random class to select random colors
    random_method = new Random();
    
    for(int i = 0; i < (args.length / 3); i++) {
      Color clr = new Color(args[i * 3], args[i * 3 + 1], args[i*3 + 2]);
      this.colors.add(clr);
      System.out.println(clr);
    }
  }
  
  public Color choose() {
    int index = random_method.nextInt(this.colors.size());
    return this.colors.get(index);
  }
  
  public Color get(int index) {
    return this.colors.get(index);
  };
};
