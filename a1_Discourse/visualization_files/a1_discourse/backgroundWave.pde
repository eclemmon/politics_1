public class BackgroundWave {
  private float xoff;
  private float yoff;
  private Color backgroundColor;
  private Color waveColor;
  private MessageQueue messageQueue;
  
  
  public BackgroundWave(Color backgroundColor, Color waveColor, MessageQueue messageQueue) {
    this.backgroundColor = backgroundColor;
    this.waveColor = waveColor;
    this.xoff = 0.0;
    this.yoff = 0.0;
    this.messageQueue = messageQueue;
  };
  
  public void render() {
    backgroundColor.background_color();
    this.messageQueue.render_messages();
    waveColor.fill_color();
    beginShape();
    this.xoff = 0;
    // Iterate over horizontal pixels
    for (float x = 0; x <= width; x += 10) {
      // Calculate a y value according to noise, map to 
      float y = map(noise(xoff, yoff), 0, 1, 750, 850); // Option #1: 2D Noise
      // float y = map(noise(xoff), 0, 1, 200,300);    // Option #2: 1D Noise
      
      // Set the vertex
      vertex(x, y); 
      // Increment x dimension for noise
      xoff += 0.05;
    }
    yoff += 0.01;
    vertex(width, height);
    vertex(0, height);
    endShape(CLOSE);
  };
};
