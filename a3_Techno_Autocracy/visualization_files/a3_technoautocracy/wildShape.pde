public class WildShape {
  private int vertices;
  private int strokeWeight;
  private Color strokeColor;
  private Color fillColor;
  private int alpha;
  
  public WildShape(int vertices, int strokeWeight, Color strokeColor, Color fillColor, int alpha) {
    this.vertices = vertices;
    this.strokeWeight = strokeWeight;
    this.strokeColor = strokeColor;
    this.fillColor = fillColor;
    this.alpha = alpha;
  };
  
  public void render() {
    this.fillColor.fill_color();
    this.strokeColor.stroke_color();
    strokeWeight(this.strokeWeight);
    beginShape();
    for (int i = 0; i < vertices; i++) {
      vertex(random(width/8, width/8*7), random(height/8, height/8*7));
    };
    endShape(CLOSE);
  };
};

public void generateShape() {
  Color sc = new Color(int(random(0, 255)), int(random(0, 255)), int(random(0, 255)));
  Color fc = new Color(int(random(0, 255)), int(random(0, 255)), int(random(0, 255)));
  WildShape ws = new WildShape(int(random(3, 7)), int(random(0, 16)), sc, fc, int(random(0, 255)));
  ws.render();
};

public void generateShapes(int n_shapes) {
  for(int i = 0; i < n_shapes; i++) {
    generateShape();
  }
};
