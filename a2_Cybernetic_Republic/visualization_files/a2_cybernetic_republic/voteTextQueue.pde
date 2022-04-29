import java.util.LinkedList;
import java.util.Queue;
import java.util.ArrayList;
import java.util.Iterator;

public class VoteTextQueue {
  private Queue<VoteText> voteTexts;
  private float voteTextStartX;
  private float voteTextStartY;
  private float init_y;
  private Color textColor;
  
  public VoteTextQueue(float init_y, Color c) {
    this.voteTexts = new LinkedList<>();
    this.voteTextStartX = width * 2;
    this.init_y = init_y;
    this.voteTextStartY = init_y;
    this.textColor = c;
  };
  
  public void add(String text) {
    VoteText voteText = new VoteText(text, "FreeMonoBold.ttf", 60, textColor, this.voteTextStartX, this.voteTextStartY + countText.get_text_height());
    this.voteTexts.add(voteText);
    this.voteTextStartX += 20 + (voteText.text_width() / 2);
    this.voteTextStartY += voteText.text_height();
  };
  
  public void remove() {
    this.voteTexts.remove();
  };
  
  public void remove_off_screen_votes() {
    for (Iterator<VoteText> iter = this.voteTexts.iterator(); iter.hasNext();) {
      VoteText voteText = iter.next();
      
      if (voteText.offScreen()) {
        iter.remove();
      };
    };
  };
  
  public void reset() {
    this.voteTextStartX = width * 2;
    this.voteTextStartY = this.init_y;
  };
  
  public void render_votes() {
    Queue<VoteText> newQueue = new LinkedList<>();
    this.remove_off_screen_votes();
    Iterator<VoteText> iter = this.voteTexts.iterator();
    while(iter.hasNext()) {
      VoteText voteText = this.voteTexts.poll();
      voteText.render();
      newQueue.add(voteText);
    };
    this.voteTexts = newQueue;
  };
  
  public void set_votes_exiting() {
    Queue<VoteText> newQueue = new LinkedList<>();
    Iterator<VoteText> iter = this.voteTexts.iterator();
    while (iter.hasNext()) {
      VoteText voteText = this.voteTexts.poll();
      voteText.set_exiting(true);
      newQueue.add(voteText);
    };
    this.voteTexts = newQueue;
  };
  
  public void update_vote_text(int index, String message) {
    int count = 0;
    Queue<VoteText> newQueue = new LinkedList<>();
    Iterator<VoteText> iter = this.voteTexts.iterator();
    while (iter.hasNext()) {
      VoteText voteText = this.voteTexts.poll();
      if (count == index) {
        voteText.setMessage(message);
      };
      newQueue.add(voteText);
      count++;
    };
    this.voteTexts = newQueue;
  };
  
  public void set_selected_vote(int index) {
    int count = 0;
    Queue<VoteText> newQueue = new LinkedList<>();
    Iterator<VoteText> iter = this.voteTexts.iterator();
    while (iter.hasNext()) {
      VoteText voteText = this.voteTexts.poll();
      if (count == index) {
        voteText.set_selected_vote(true);
      };
      newQueue.add(voteText);
      count++;
    };
    this.voteTexts = newQueue;
    
  };
  
  public VoteText peek() {
    return this.voteTexts.peek();
  };
  
};
