public class MessageQueue {
  private Queue<Message> messages;

  public MessageQueue() {
    this.messages = new LinkedList<>();
  };
  
  public void add(Message message) {
    this.update_messages_y_targets(message);
    this.messages.add(message);
  };
  
  public void remove() {
    this.messages.remove();
  };
  
  public void remove_invisible_messages() {
    for(Iterator<Message> iter = this.messages.iterator(); iter.hasNext();) {
      Message item = iter.next();
      
      if (item.invisible() == true) {
        iter.remove();
      };
    };
  };
  
  public void remove_out_of_bounds_messages() {
    for(Iterator<Message> iter = this.messages.iterator(); iter.hasNext();) {
      Message item = iter.next();
      
      if (item.get_out_of_bounds() == true) {
        iter.remove();
      };
    };
  };
  
  public void update_messages_y_targets(Message message) {
    for(Iterator<Message> iter = this.messages.iterator(); iter.hasNext();) {
      Message item = iter.next();
      item.set_y_target(item.get_y_target() - message.get_textHeight());
    };
  };
  
  public void render_messages() {
    // Create new Queue;
    Queue<Message> newQueue = new LinkedList<>();
    // Remove the out of bounds messages
    this.remove_out_of_bounds_messages();
    // Iterator over the arrows
    Iterator<Message> itr = this.messages.iterator();
    while(itr.hasNext()) {
      Message message = this.messages.poll();
      message.render();
      newQueue.add(message);
    };
    this.messages = newQueue;
  };
  
  
  
};
