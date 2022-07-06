import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;
import java.util.Iterator;

public class AttackQueue {
  private Queue<Attack> attacks;

  public AttackQueue() {
    this.attacks = new LinkedList<>();
  };
  
  public void add(Attack attack) {
    this.attacks.add(attack);
  };
  
  public void remove() {
    this.attacks.remove();
  };
  
  public void remove_invisible_attacks() {
    for(Iterator<Attack> iter = this.attacks.iterator(); iter.hasNext();) {
      Attack item = iter.next();
      
      if (item.invisible() == true) {
        iter.remove();
      };
    };
  };
  
  public void render_attacks() {
    // Create new Queue;
    Queue<Attack> newQueue = new LinkedList<>();
    // Remove the invisible arrows
    this.remove_invisible_attacks();
    // Iterator over the arrows
    Iterator<Attack> itr = this.attacks.iterator();
    while(itr.hasNext()) {
      Attack attack = this.attacks.poll();
      attack.render();
      newQueue.add(attack);
    };
    this.attacks = newQueue;
  };
  
  
};

public class Attack {
  private Color clr;
  private int current_alpha;
  private int speed;
  
  public Attack() {
    this.clr = new Color(255,255,255);
    this.current_alpha = 255;
    this.speed = 30;
  };
  
  public void render() {
    this.update_alpha();
    this.clr.fill_color_with_alpha(this.current_alpha);
    rect(0, 0, 1920, 900);
  };
  
  public void update_alpha() {
    this.current_alpha = this.current_alpha - this.speed;
  };
  
  public boolean invisible() {
    return this.current_alpha <= 0;
  };
};
