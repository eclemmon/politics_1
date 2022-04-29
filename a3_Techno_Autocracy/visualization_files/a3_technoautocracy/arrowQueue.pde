import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;
import java.util.Iterator;

public class ArrowQueue {
  private Queue<Arrow> arrows;

  public ArrowQueue() {
    this.arrows = new LinkedList<>();
  };
  
  public void add(Arrow arrow) {
    this.arrows.add(arrow);
  };
  
  public void remove() {
    this.arrows.remove();
  };
  
  public void remove_invisible_arrows() {
    for(Iterator<Arrow> iter = this.arrows.iterator(); iter.hasNext();) {
      Arrow item = iter.next();
      
      if (item.invisible() == true) {
        iter.remove();
      };
    };
  };
  
  public void render_arrows() {
    // Create new Queue;
    Queue<Arrow> newQueue = new LinkedList<>();
    // Remove the invisible arrows
    this.remove_invisible_arrows();
    // Iterator over the arrows
    Iterator<Arrow> itr = this.arrows.iterator();
    while(itr.hasNext()) {
      Arrow arrow = this.arrows.poll();
      arrow.render();
      newQueue.add(arrow);
    };
    this.arrows = newQueue;
    
  };
  
  
};
