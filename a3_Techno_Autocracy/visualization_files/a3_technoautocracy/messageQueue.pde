public class MessageQueue {
  private Queue<Message> messages;

  public MessageQueue() {
    this.messages = new LinkedList<>();
  };
  
  public void add(Message message) {
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
  
  public void render_messages() {
    // Create new Queue;
    Queue<Message> newQueue = new LinkedList<>();
    // Remove the invisible arrows
    this.remove_invisible_messages();
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
